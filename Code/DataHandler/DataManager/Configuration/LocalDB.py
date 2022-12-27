import json, traceback
from json import JSONDecodeError
from Code.Model.Payment.Payment import Payment
from Code.Model.Car.ParkingSlot import ParkingSlot


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
            try:
                jsonStreamRead = open(LocalDB.SUPPORTED_MEDIA[self.type], "r")
                try:
                    dataJson = json.load(jsonStreamRead)
                except JSONDecodeError:
                    dataJson = []
                jsonStreamRead.close()

                jsonStreamWrite = open(LocalDB.SUPPORTED_MEDIA[self.type], "w")
                dataJson.append(paymentObject.__dict__)
                jsonStreamWrite.truncate(0)
                jsonStreamWrite.write(json.dumps(dataJson, indent=4))
                jsonStreamWrite.close()
                return True, ''
            except Exception as e:
                traceback.print_exc()
                return False, f'Error with "updatePayment": {e}'
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
                    output = []
                    for payment in dataJson:
                        if payment.get("licensePlate","")==licensePlate:
                            output.append(Payment(paymentSerialized=payment))
                    return True, output
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
            jsonStreamRead = open(LocalDB.SUPPORTED_MEDIA[self.type], "r")
            try:
                dataJson = json.load(jsonStreamRead)
            except JSONDecodeError:
                dataJson = []
            jsonStreamRead.close()

            jsonStreamWrite = open(LocalDB.SUPPORTED_MEDIA[self.type], "w")
            for index in range(len(dataJson)):
                if dataJson[index].get("transactionID","")==paymentObject.transactionID:
                    dataJson[index] = paymentObject.__dict__
            jsonStreamWrite.truncate(0)
            jsonStreamWrite.write(json.dumps(dataJson, indent=4))
            jsonStreamWrite.close()
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
                    return True, [ParkingSlot(parkingslotSerialized=data)
                                  for data in jsonData]
                except JSONDecodeError:
                    return True, []
        except Exception as e:
            return False, f'Error with "getParkingSlot": {e}'

    def checkParkingSlots(self):
        """
        The method cheks whether or not there are any parking slost available.

        (True, int, int) is returned if no error is found, (True, number of slots available, first id available)

        (False, str, '') is returned if an error is found: the string contains the error

        @return: (True, int, int) or (False, str, str)
        """
        check, slots = self.getParkingSlot()
        if not check:
            return False, str(slots), ''
        if check is True and slots == []:
            return False, "Error with loading parking: no parking slots exist", ''

        available = 0
        id = 0
        for parkingSlot in slots:
            if parkingSlot.state is True:
                available += 1
                if available == 1:
                    id = parkingSlot.id
        return True, available, id
