import json
from Code.Model.Payment import Payment


class LocalDB:
    """This class defines methods required to store/read/update data inside configuration file.
    We should reset each night payament.json, anyway..."""

    SUPPORTED_MEDIA = {"PAYMENTS":"Configuration/LocalDB/payments.json"}

    def __init__(self,type):
        """type is the media that we want to handle calling the class.
        Calling the constructor i check if the media type is supported.
        """
        if type not in LocalDB.SUPPORTED_MEDIA:
            raise Exception("Requested media type is not supported")
        else:
            self.type = type

    """Methods to handle payments"""
    def addPayment(self, paymentObject):
        """This add a payment to payaments.json file with given payment instance
        True,'' is returned if everything is ok otherwise False,STR is returned
        """
        try:
            with open(LocalDB.SUPPORTED_MEDIA[self.type],"r") as jsonStream:
                dataJson = json.load(jsonStream)
                dataJson.append(paymentObject.toJson())
                json.dump(dataJson, jsonStream)
            return True, ''
        except Exception as e:
            return False, f'Error with "addPayamemt": {e}'

    def getPaymentByLicense(self, licensePlate):
        """This method return a payment instance
        True,istance is returned if everything is ok otherwise False,STR is returned.
        If no payments if found True, None is returned.
        """
        try:
            with open(LocalDB.SUPPORTED_MEDIA[self.type], "r") as jsonStream:
                dataJson = json.load(jsonStream)
                for payment in dataJson:
                    if payment.get("licensePlate","")==licensePlate:
                        return True, Payment(paymentSerialized=payment)
            return True, None
        except Exception as e:
            return False, f'Error with "getPayamemtByLicense": {e}'

    def getPaymentByTransactionID(self, transactionID):
        """This method return a payment instance
        True,istance is returned if everything is ok otherwise False,STR is returned.
        If no payments if found True, None is returned.
        """
        try:
            with open(LocalDB.SUPPORTED_MEDIA[self.type], "r") as jsonStream:
                dataJson = json.load(jsonStream)
                for payment in dataJson:
                    if payment.get("transactionID","")==transactionID:
                        return True, Payment(paymentSerialized=payment)
            return True, None
        except Exception as e:
            return False, f'Error with "getPayamemtByTransactionID": {e}'

    def updatePayment(self, paymentObject):
        """This method update a payment searching for ID with given payment instance
        True,'' is returned if everything is ok otherwise False,STR is returned
        """
        try:
            with open(LocalDB.SUPPORTED_MEDIA[self.type],"r") as jsonStream:
                dataJson = json.load(jsonStream)
                newDataJson = []
                for payment in dataJson:
                    if payment.get("transactionID","")==paymentObject.transactionID:
                        newDataJson.append(paymentObject.toJson())
                    else:
                        newDataJson.append(payment)

                json.dump(newDataJson, jsonStream)
            return True, ''
        except Exception as e:
            return False, f'Error with "updatePayment": {e}'