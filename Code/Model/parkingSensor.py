import json
from datetime import datetime
from six import string_types
from car import CarDescriptor

class ParkingSensorDescriptor:
    """
    ParkingSensorDescriptor is a model of a license plate sensor for the Smart Parking
    """

    def __init__(self, parkingPlace):
        self.parkingPlace = parkingPlace
        self.car = CarDescriptor()
        self.readingTime = 0
        self.error = False

    def readThePlate(self, car):
        if isinstance(car, CarDescriptor):
            self.car = car
            self.readingTime = datetime.now()
        else:
            raise ValueError("Data passed as paramether must be a CarDescriptor class data")

    def setErrorTrue(self):
        self.error = True

    def setErrorFalse(self):
        self.error = False

    def to_json(self):
        json.dumps(self, default=lambda o: o.__dict__())
