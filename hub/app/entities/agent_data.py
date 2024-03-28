from datetime import datetime
from pydantic import BaseModel, model_validator
import logging


class AccelerometerData(BaseModel):
    x: float
    y: float
    z: float


class GpsData(BaseModel):
    latitude: float
    longitude: float


class AgentData(BaseModel):
    user_id: int
    accelerometer: AccelerometerData
    gps: GpsData
    timestamp: datetime
    
    # @model_validator(mode='before')
    # @classmethod
    # def parse_timestamp(cls, data):
    #     # Convert the timestamp to a datetime object
    #     if isinstance(data['timestamp'], datetime):
    #         pass
    #     else:
    #         try:
    #             data['timestamp'] = datetime.fromisoformat(data['timestamp'].ljust(26, '0'))
    #         except (TypeError, ValueError):
    #             raise ValueError(
    #                 "Invalid timestamp format. Expected ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)."
    #             )
    #     return data
