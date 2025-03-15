from database import Database


class Config:
    SENSORS = ["temperature", "humidity", "light"]


db = Database(Config.SENSORS)

