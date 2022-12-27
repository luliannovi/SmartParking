import aiocoap.resource as resource

from Code.DataHandler.DataManager.Configuration.LocalDB import LocalDB
from Code.Model.Monitor.Monitor import Monitor


class EntryMonitor(resource.Resource):
    """The class represents the resource monitor for parking entrance"""

    def __init__(self, localDB):
        """The construct needs a LocalDB object in order to check parking slots and operate on them."""
        super().__init__()
        self.Monitor = Monitor()
        self.localDB = localDB

    def getFirstFreeSlot(self):
        """The method checks if any parking slot is available.
        Raises errors if LocalDB methods checkParkingSlots() returns any errors.
        Otherwise, returns (number of slots available, ID of first slot available)"""
        check, num, firstID = self.localDB.checkParkingSlots()
        if not check:
            raise Exception(str(num))
        return num, firstID

    def render_get(self, request):
        pass

    def render_put(self, request):
        pass

    def render_post(self, request):
        pass
