import json, traceback
from json import JSONDecodeError
from Code.Model.Payment.Payment import Payment
from Code.Model.Car.ParkingSlot import ParkingSlot
from Code.Logging.Logger import loggerSetup

logger = loggerSetup("db", "Code/Logging/DB/db.log")


class LocalDB:
    """This class defines methods required to store/read/update data inside configuration file.
    We should reset each night payament.json, anyway..."""

    SUPPORTED_MEDIA = {
        "PAYMENTS": "Configuration/LocalDB/payments.json",
        "PARKING_SLOT": "Configuration/LocalDB/parkingSlot.json",
        "CAR": "Configuration/LocalDB/car.json"
    }

    def __init__(self, type):
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
                logger.error(e)
                return False, f'Error with "updatePayment": {e}'
            return True, ''
        except Exception as e:
            logger.error(e)
            return False, f'Error with "addPaymemt": {e}'

    def getPaymentByLicense(self, licensePlate):
        """This method return a payment instance
        True,instance is returned if everything is ok otherwise False,STR is returned.
        If no payments if found True, None is returned.
        """
        try:
            with open(LocalDB.SUPPORTED_MEDIA[self.type], "r") as jsonStream:
                try:
                    dataJson = json.load(jsonStream)
                    output = []
                    for payment in dataJson:
                        if payment.get("licensePlate", "") == licensePlate:
                            output.append(Payment(paymentSerialized=payment))
                    return True, output
                except JSONDecodeError:
                    return True, None
            return True, None
        except Exception as e:
            logger.error(e)
            return False, f'Error with "getPaymentByLicense": {e}'

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
                        if payment.get("transactionID", "") == transactionID:
                            return True, Payment(paymentSerialized=payment)
                except JSONDecodeError:
                    return True, None
            return True, None
        except Exception as e:
            logger.error(e)
            return False, f'Error with "getPayamemtByTransactionID": {e}'

    def removePaymentByLicense(self, licensePlate):
        """This method remove all payments from payments.json containing specific licensePlate.
        Retrun True, '' if everything is right; otherwise False, erroString
        """
        try:
            jsonStreamRead = open(LocalDB.SUPPORTED_MEDIA[self.type], "r")
            try:
                dataJson = json.load(jsonStreamRead)
            except JSONDecodeError:
                dataJson = []
            jsonStreamRead.close()

            jsonStreamWrite = open(LocalDB.SUPPORTED_MEDIA[self.type], "w")
            filtered = [element for element in dataJson if element['licensePlate'] != licensePlate]
            jsonStreamWrite.truncate(0)
            jsonStreamWrite.write(json.dumps(filtered, indent=4))
            jsonStreamWrite.close()
            return True, ''
        except Exception as e:
            logger.error(e)
            return False, f'Error with "removePaymentByLicense": {e}'

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
                if dataJson[index].get("transactionID", "") == paymentObject.transactionID:
                    dataJson[index] = paymentObject.__dict__
            jsonStreamWrite.truncate(0)
            jsonStreamWrite.write(json.dumps(dataJson, indent=4))
            jsonStreamWrite.close()
            return True, ''
        except Exception as e:
            logger.error(e)
            return False, f'Error with "updatePayment": {e}'

    """Methods that read each position"""

    def getParkingSlotById(self, givenId):
        """This method return a parking slot by the given id.
        If there is no item an empty list will be returned.
        For a list of parking slot -> True, parkingSlot.
        For an error -> False, stringError.
        For a empty parking slot file -> True, []"""

        try:
            with open(LocalDB.SUPPORTED_MEDIA[self.type], "r") as jsonStream:
                try:
                    jsonData = json.load(jsonStream)
                    for data in jsonData:
                        if data['id'] == givenId:
                            return True, data
                    return True, []
                except JSONDecodeError:
                    return True, []
        except Exception as e:
            logger.error(e)
            return False, f'Error with "getParkingSlot": {e}'

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
            logger.error(e)
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
            if parkingSlot.state is False:
                available += 1
                if available == 1:
                    id = parkingSlot.id
        return True, available, id

    def updateParkingSlot(self, parkingSlot):
        """
        the method gets updates about a single parkingSlot (free/taken) with a string that contains the plate
        """
        try:
            # mio
            jsonStreamRead = open(LocalDB.SUPPORTED_MEDIA[self.type], "r")
            try:
                dataJson = json.load(jsonStreamRead)
            except JSONDecodeError:
                dataJson = []
            jsonStreamRead.close()

            jsonStreamWrite = open(LocalDB.SUPPORTED_MEDIA[self.type], "w")
            for index in range(len(dataJson)):
                if dataJson[index].get("id", "") == parkingSlot.id:
                    dataJson[index] = parkingSlot.__dict__
                    dataJson[index]["state"] = str(dataJson[index]["state"])
            jsonStreamWrite.truncate(0)
            jsonStreamWrite.write(json.dumps(dataJson, indent=4))
            jsonStreamWrite.close()
            return True, ''

        except Exception as e:
            logger.error(e)
            return False, f'Error with "addParkingSlot": {e}'

    """Methods that handles car.json update"""

    def updateExitTime(self, plate, exitTime):
        """
        The method permit to insert the exit time for a car leaving a specific parking slot.

        :return: (False, errorString) if errors occurs, (True, '') otherwise.
        """
        try:
            jsonStreamRead = open(LocalDB.SUPPORTED_MEDIA[self.type], "r")
            try:
                dataJson = json.load(jsonStreamRead)
            except JSONDecodeError:
                dataJson = []
            jsonStreamRead.close()

            jsonStreamWrite = open(LocalDB.SUPPORTED_MEDIA[self.type], "w")
            found = False
            for index in range(len(dataJson)):
                if dataJson[index].get("plate", "") == plate:
                    slots = dataJson[index].get("slots", None)
                    found = True
                    slots[len(slots) - 1]["exitTime"] = exitTime

            if not found:
                return False, "no car with that plate founded in memory"
            jsonStreamWrite.truncate(0)
            jsonStreamWrite.write(json.dumps(dataJson, indent=4))
            jsonStreamWrite.close()
            return True, ''
        except Exception as e:
            logger.error(str(e))
            return False, f'Error with "insertParkedCar": {e}'

    def insertParkedCar(self, plate, parkingSlotID, entryTime, exitTime):
        """
        The method handles a car parking in a parking slot. Either a car that just entered the parking and a car that is
        changing the slot.

        :return: (False, str) if error occurs, (True, '') otherwise.
        """
        try:
            jsonStreamRead = open(LocalDB.SUPPORTED_MEDIA[self.type], "r")
            try:
                dataJson = json.load(jsonStreamRead)
            except JSONDecodeError:
                dataJson = []
            jsonStreamRead.close()

            jsonStreamWrite = open(LocalDB.SUPPORTED_MEDIA[self.type], "w")
            found = False
            for index in range(len(dataJson)):
                if dataJson[index].get("plate", "") == plate:
                    slots = dataJson[index].get("slots", None)
                    found = True
                    slots[len(slots) - 1]["exitTime"] = exitTime
                    jsonAdd = {
                        "id": parkingSlotID,
                        "entryTime": entryTime,
                        "exitTime": -1
                    }
                    slots.append(jsonAdd)
            if not found:
                jsonAdd = {
                    "plate": plate,
                    "slots": [{
                        "id": parkingSlotID,
                        "entryTime": entryTime,
                        "exitTime": -1
                    }
                    ]
                }
                dataJson.append(jsonAdd)
            jsonStreamWrite.truncate(0)
            jsonStreamWrite.write(json.dumps(dataJson, indent=4))
            jsonStreamWrite.close()
            return True, ''
        except Exception as e:
            logger.error(str(e))
            return False, f'Error with "insertParkedCar": {e}'

    def removeParkedCar(self, plate):
        """
        Method is used to remove a parked car.
        It needs the plate (str) of the car that needs to be removed.

        :return: (False, str) if errore occurs, (True, '') if no car is found, (True, json_removed) if the car is removed
        (note that in this case the json removed is returned in order to do any operations with id (as getting first entryTime).
        """
        try:
            jsonStreamRead = open(LocalDB.SUPPORTED_MEDIA[self.type], "r")
            try:
                dataJson = json.load(jsonStreamRead)
            except JSONDecodeError:
                dataJson = []
            jsonStreamRead.close()

            jsonStreamWrite = open(LocalDB.SUPPORTED_MEDIA[self.type], "w")
            removed = ''
            for index in range(len(dataJson)):
                if dataJson[index].get("plate", "") == plate:
                    removed = dataJson.pop(index)

            jsonStreamWrite.truncate(0)
            jsonStreamWrite.write(json.dumps(dataJson, indent=4))
            jsonStreamWrite.close()
            return True, removed
        except Exception as e:
            logger.error(str(e))
            return False, f'Error with "insertParkedCar": {e}'
