import json
from datetime import datetime


class Payament:
    """Payment model a received payment from CLOUD service
    """

    def __init__(self, transactionID="", licensePlate="", timeIn=None, paymentTime=None, total=0.00, paymentSerialized=None):
        """- transactionID is the ID given from the supposed PAYMENT gateway
        - licensePlate is the plate refered to the payment
        - timeIn is the time (datetime.now() format) when the car entered
        - paymentTime is the time (datetime.now() format) when the user made the payment
        - total is the amount of money due to car parking receipt
        - paymentStored is the time when the object is created.
        - timeOut is the time when the car reach the out-gate

        If payamentSerialized is not None the the constructor set as class variable all the keys inside json serialized payment"""

        self.transactionID = transactionID
        self.licensePlate = licensePlate
        self.timeIn = timeIn
        self.timeOut = None
        self.paymentTime = paymentTime
        self.total = round(float(total),2)


        if paymentSerialized is not None:
            self.__dict__ = paymentSerialized

    def setOutTime(self, timeOut):
        """If payment has been processed at the gate i set the outTime"""
        if isinstance(timeOut, datetime):
            self.timeOut = timeOut
        else:
            raise Exception(f"{timeOut} is not a valid DateTime object")

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__())