import json
from datetime import datetime
from Car.Car import Car


class ParkingSensor:
    """
    ParkingSensor is a model of a license plate sensor for the Smart Parking
    """

    def __init__(self, parkingPlace):
        self.parkingPlace = parkingPlace
        self.car = None
        self.readingTime = 0
        self.error = False

    def readThePlate(self, carPlate):
        if isinstance(carPlate, str):
            self.car = Car(None,carPlate)
            self.readingTime = datetime.now()
        else:
            raise ValueError("Data passed as paramether must be a CarDescriptor class data")

    def setErrorTrue(self):
        self.error = True

    def setCar(self, car):
        self.car = car

    def getParkingPlace(self):
        return self.parkingPlace

    def setErrorFalse(self):
        self.error = False

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__())
