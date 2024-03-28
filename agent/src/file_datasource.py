from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
from domain.parking import Parking
import config


class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
        parking_filename: str,
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        try:
            x, y, z = self.ax.__next__()
        except:
            self.accelerometer_file.seek(0,0)
            x, y, z = self.ax.__next__()
            x, y, z = self.ax.__next__()
        try:
            lg, lt = self.gps.__next__()
        except:
            self.gps_file.seek(0,0)
            lg, lt = self.gps.__next__()
            lg, lt = self.gps.__next__()
        try:
            p = self.park.__next__()[0]
        except:
            self.parking_file.seek(0,0)
            p = self.park.__next__()[0]
            p = self.park.__next__()[0]
        return AggregatedData(
            Accelerometer(x,y,z),
            Gps(lg,lt),
            Parking(p, Gps(lg,lt)),
            datetime.now(),
            config.USER_ID,
        )

    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        self.accelerometer_file = open(self.accelerometer_filename, newline='')
        self.gps_file = open(self.gps_filename, newline='')
        self.parking_file = open(self.parking_filename, newline='')
        self.ax = reader(self.accelerometer_file, delimiter=',', quotechar='|')
        self.gps = reader(self.gps_file, delimiter=',', quotechar='|')
        self.park = reader(self.parking_file, delimiter=',', quotechar='|')
        self.ax.__next__() 
        self.gps.__next__()
        self.park.__next__()

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        self.accelerometer_file.close()
        self.gps_file.close()
        self.parking_file.close()
