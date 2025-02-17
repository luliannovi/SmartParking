from datetime import datetime
import json


class ExitSensor:
    """
    ExitSensor is a model of a license plate sensor for the Smart Parking
    """

    def __init__(self):
        self.carPlate = ""
        self.readingTime = 0
        self.error = False

    def readThePlate(self, carPlate):
        """
        Method used to notify a new plate reading.
        """
        if isinstance(carPlate, str):
            self.carPlate = carPlate
            self.readingTime = float(datetime.timestamp(datetime.now()))
        else:
            raise ValueError("Data passed as paramether must be a CarDescriptor class data")

    def setErrorTrue(self):
        self.error = True

    def setErrorFalse(self):
        self.error = False

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
