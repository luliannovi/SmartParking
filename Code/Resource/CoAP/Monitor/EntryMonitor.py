import aiocoap.resource as resource

from Code.DataHandler.DataManager.Configuration.LocalDB import LocalDB
from Code.Model.Monitor.Monitor import Monitor


class EntryMonitor(resource.Resource):
    """The class represents the resource monitor for parking entrance"""

    def __init__(self, monitorID, description, localDB):
        """The construct needs a LocalDB object in order to check parking slots and operate on them."""
        super().__init__()
        self.Monitor = Monitor(monitorID, description)
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
        """
        TODO: return '<state>;<display>'
        Ovvero deve ritornare lo stato (on off) e poi quello che sta mostrando (numero posti/ niente/ primo libero)
        """
        pass

    def render_put(self, request):
        """
        TODO: paylaod_body='<state>;<display>' OPPURE (meglio) gestione da DataManager
        1) La richiesta deve contenere lo stato nel quale lo si vuole settare e anche cosa deve mostrare.
        2) DataManager, nel momento in cui leggo una modifica da plate reader invio al monitor cosa mostrare
        """
        pass

    def render_post(self, request):
        """
        TODO: switch dello stato
        """
        pass
