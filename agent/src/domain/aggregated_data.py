from dataclasses import dataclass
from domain.parking import Parking
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps


@dataclass
class AggregatedData:
    accelerometer: Accelerometer
    gps: Gps
    parking: Parking
    timestamp: datetime
    user_id: int
