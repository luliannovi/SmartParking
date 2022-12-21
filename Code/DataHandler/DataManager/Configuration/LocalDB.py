import json, traceback
from json import JSONDecodeError
from Code.Model.Payment.Payment import Payment


class LocalDB:
    """This class defines methods required to store/read/update data inside configuration file.
    We should reset each night payament.json, anyway..."""

    SUPPORTED_MEDIA = {
        "PAYMENTS":"Configuration/LocalDB/payments.json",
        "PARKING_SLOT":"Configuration/LocalDB/parkingSlot.json"
   }

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
            with open(LocalDB.SUPPORTED_MEDIA[self.type],"r+") as jsonStream:
                try:
                    dataJson = json.load(jsonStream)
                except JSONDecodeError:
                    dataJson = []
                dataJson.append(paymentObject.__dict__)
                json.dump(dataJson, jsonStream, indent=4)
            return True, ''
        except Exception as e:
            traceback.print_exc()
            return False, f'Error with "addPayamemt": {e}'

    def getPaymentByLicense(self, licensePlate):
        """This method return a payment instance
        True,istance is returned if everything is ok otherwise False,STR is returned.
        If no payments if found True, None is returned.
        """
        try:
            with open(LocalDB.SUPPORTED_MEDIA[self.type], "r") as jsonStream:
                try:
                    dataJson = json.load(jsonStream)
                    for payment in dataJson:
                        if payment.get("licensePlate","")==licensePlate:
                            return True, Payment(paymentSerialized=payment)
                except JSONDecodeError:
                    return True, None
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
                try:
                    dataJson = json.load(jsonStream)
                    for payment in dataJson:
                        if payment.get("transactionID","")==transactionID:
                            return True, Payment(paymentSerialized=payment)
                except JSONDecodeError:
                    return True, None
            return True, None
        except Exception as e:
            traceback.print_exc()
            return False, f'Error with "getPayamemtByTransactionID": {e}'

    def updatePayment(self, paymentObject):
        """This method update a payment searching for ID with given payment instance
        True,'' is returned if everything is ok otherwise False,STR is returned
        """
        try:
            with open(LocalDB.SUPPORTED_MEDIA[self.type],"r+") as jsonStream:
                try:
                    dataJson = json.load(jsonStream)
                except JSONDecodeError:
                    dataJson = []
                newDataJson = []
                for payment in dataJson:
                    if payment.get("transactionID","")==paymentObject.transactionID:
                        newDataJson.append(paymentObject.toJson())
                    else:
                        newDataJson.append(payment)

                json.dump(newDataJson, jsonStream, indent=4)
            return True, ''
        except Exception as e:
            traceback.print_exc()
            return False, f'Error with "updatePayment": {e}'

    """Methods that read each position"""
    def getParkingSlot(self):
        """This method return all the json object stored inside.
        If there is no item an empty list will be returned.
        For a list of parking slot -> True, [parkingslotObject].
        For an error -> False, stringError.
        For a empty parking slot file -> True, []"""
        try:
            with open(LocalDB.SUPPORTED_MEDIA[self.type], "r") as jsonStream:
                try:
                    jsonData = json.load(jsonStream)
                    #TODO -> REPLACE WITH THE OBJECT INSTANCE
                    return True, [jsonData[key] for key in jsonData]
                except JSONDecodeError:
                    return True, []
        except Exception as e:
            return False, f'Error with "getParkingSlot": {e}'