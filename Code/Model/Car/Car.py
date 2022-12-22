import random
import json
import time
from datetime import datetime



class Car:
    """Car is a model for cars inside the SmartParking"""

    def __init__(self, carSerialized=None):
        self.licensePlate = ""
        self.parkingSlot = None
        self.paid = False
        self.entryTime = datetime.now()
        self.exitTime = 0
        self.deltaTime = 0
        if carSerialized is not None:
            self.__dict__ = dict(carSerialized)

    def calculateDeltaTime(self):
        """
        Set the difference between entry time and exit time
        Return False if the car is not out yet
        """
        if isinstance(self.exitTime, datetime):
            self.deltaTime = (self.exitTime - self.entryTime).min
        else:
            raise ValueError("The car has not an exit time yet")

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__())

    def exitNow(self):
        """
        Set the exit time to the current time
        """
        self.exitTime = datetime.now()
        self.calculateDeltaTime()

    def setPaid(self):
        self.paid = True

    def setEntryTime(self,datetimeObject):
        """If entryTime is datetime I set it, otherwise i convert it from timestamp"""
        if isinstance(datetimeObject, datetime.__class__):
            self.entryTime = datetimeObject
        else:
            self.entryTime = datetime.fromtimestamp(datetimeObject)

    def setLicensePlate(self, licensePlate):
        if isinstance(licensePlate, str):
            self.licensePlate = licensePlate
        else:
            raise ValueError("Data passed as parameter must be a String")

    def setParkingSlot(self, parkingSlot):
        from Code.Model.Car.ParkingSlot import ParkingSlot
        if isinstance(parkingSlot, ParkingSlot):
            self.parkingSlot = parkingSlot
        else:
            raise ValueError("Data passed as parameter must be an instance of parkingSlot")
