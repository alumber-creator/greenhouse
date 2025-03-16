from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: str | None = None
    role: str | None = "user"
    created_at: datetime | None = None


class SensorData(BaseModel):
    sensor_id: str
    value: float
    timestamp: datetime
