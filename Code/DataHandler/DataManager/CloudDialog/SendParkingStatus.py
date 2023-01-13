from Code.DataHandler.DataManager.Configuration.LocalDB import LocalDB
from Code.Model.DB.DataBase import DataBase
import json


class SendParkingStatus:
    """This class allows to read incoming payments coming from cloud services
    """

    def __init__(self):
        """Constructor build the object that send data to Azure IoT
        """
        self.type = type
        self.reference = "/parkingStatus"
        self.url = "https://smartparking-47679-default-rtdb.europe-west1.firebasedatabase.app/parkingStatus"
        self.db = DataBase(self.reference, self.url)

    def sendStatus(self, dictParkingStatus):
        """This method detect if position is already stored or if it's new.
        Data expected in the same format of parkingSlot.json"""
        id = dictParkingStatus["parkingId"]
        self.db.update(id, dictParkingStatus) if self.db.check(id) else self.db.add(id, dictParkingStatus)

"""#TEST
lDb = LocalDB("PARKING_SLOT")
check, output = lDb.getParkingSlot()
if check:
    sps = SendParkingStatus()
    for parkingSlot in output:
        sps.sendStatus(eval(str(parkingSlot)))"""




