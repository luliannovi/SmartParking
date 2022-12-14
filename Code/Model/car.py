import random
import json
import time
from datetime import datetime
from six import string_types


class CarDescriptor:
    """CarDescriptor is a model for cars inside the SmartParking"""

    def __init__(self):
        self.licensePlate = ""
        self.parkingPlace = ""
        self.paid = False
        self.entryTime = datetime.now()
        self.exitTime = 0
        self.deltaTime = 0

    def calculateDeltaTime(self):
        """
        Set the difference between entry time and exit time
        Return False if the car is not out yet
        """
        if isinstance(self.exitTime, datetime):
            self.deltaTime = (self.exitTime - self.entryTime).min
            return True
        else:
            return False

    def to_json(self):
        json.dumps(self, default=lambda o: o.__dict__())

    def exitNow(self):
        """
        Set the exit time to the current time
        """
        self.exitTime = datetime.now()
        self.calculateDeltaTime()

    def setPaid(self):
        self.paid = True

    def setLicensePlate(self, licensePlate):
        if isinstance(licensePlate, string_types):
            self.licensePlate = licensePlate
            return True
        else:
            return False

    def setParkingPlace(self, parkingPlace):
        if isinstance(parkingPlace, string_types):
            self.parkingPlace = parkingPlace
            return True
        else:
            return False
