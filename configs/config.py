from database import Database


class Config:
    SENSORS = ["temperature", "humidity", "light"]

    CHECK_OPTIONS = [
        ("check1", "Уведомления о критических ситуациях"),
        ("check2", "Уведомления о выполнении операций"),
        ("check3", "Уведомления с рекомендациями"),
    ]


db = Database(Config.SENSORS)

