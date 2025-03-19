import threading
import logging
import time
from datetime import datetime

import cv2
import os

from config import Config



class VideoRecorder:
    def __init__(self):
        self.segments = []
        self.lock = threading.Lock()
        self.running = False
        self.cap = None
        self.writer = None
        self.segment_start = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def _record(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            logging.error("Cannot open camera")
            return

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.RESOLUTION[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.RESOLUTION[1])

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                logging.warning("Can't receive frame")
                continue

            if self.writer is None or time.time() - self.segment_start > Config.SEGMENT_DURATION:
                self._create_new_segment()

            self.writer.write(frame)

        self._cleanup()

    def _create_new_segment(self):
        if self.writer is not None:
            self.writer.release()

        filename = f"segment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
        self.writer = cv2.VideoWriter(
            filename,
            cv2.VideoWriter_fourcc(*'XVID'),
            Config.FPS,
            Config.RESOLUTION
        )
        self.segment_start = time.time()

        with self.lock:
            self.segments.append(filename)
            while len(self.segments) > Config.MAX_SEGMENTS:
                old = self.segments.pop(0)
                if os.path.exists(old):
                    os.remove(old)

    def get_segments(self):
        with self.lock:
            return self.segments.copy()

    def _cleanup(self):
        if self.writer is not None:
            self.writer.release()
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()


recorder = VideoRecorder()