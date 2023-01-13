import time

import aiocoap
import aiocoap.resource as resource
import aiocoap.numbers as numbers
from aiocoap import Code

from kpn_senml import *

from Code.DataHandler.DataManager.Configuration.LocalDB import LocalDB
from Code.Model.Monitor.Monitor import Monitor


class EntryMonitor(resource.Resource):
    """The class represents the resource monitor for parking entrance"""

    def __init__(self, monitorID, description, localDB):
        """The construct needs a LocalDB object in order to check parking slots and operate on them."""
        super().__init__()
        self.monitorID = monitorID
        self.description = description

        self.monitor = Monitor(monitorID, description)
        self.localDB = localDB
        # interface actuator
        self.if_ = 'core.a'
        # resource type
        self.rt = 'it.resource.actuator.monitor'
        # content type
        self.ct = numbers.media_types_rev['application/senml+json']

    # ------------------------------ DA CANCELLARE ------------------------------
    # def getFirstFreeSlot(self):
    #     """The method checks if any parking slot is available.
    #     Raises errors if LocalDB methods checkParkingSlots() returns any errors.
    #     Otherwise, returns (number of slots available, ID of first slot available)"""
    #     check, num, firstID = self.localDB.checkParkingSlots()
    #     if not check:
    #         raise Exception(str(num))
    #     return num, firstID
    # ---------------------------------------------------------------------------

    def buildSenMLJson(self):
        """
        The method creates a senml+json representation of the resource entry monitor.
        The response contains 2 records in a single pack. The first one is "State" and contains the state of the monitor
        (on/off), the second one is "Display" and contains the string displayed in the monitor. There's a base name
        which is "EntryMonitor".
        """
        state = self.monitor.state
        display = self.monitor.display
        pack = SenmlPack(self.monitor.monitorID)
        state_record = SenmlRecord("State",
                                   bn="EntryMonitor",
                                   unit="bool",
                                   value=state,
                                   time=int(time.time()))
        display_record = SenmlRecord("Display",
                                     unit="str",
                                     value=display,
                                     time=int(time.time()))
        pack.add(state_record)
        pack.add(display_record)
        return pack.to_json()

    async def render_get(self, request):
        """
        Methods handles GET request.
        See method self.buildSenMLJson() in interested in payload content.
        """
        print("EntryMonitor with ID: " + self.monitorID + " --> GET Request Received...")
        payload = self.buildSenMLJson()
        return aiocoap.Message(content_format=self.ct, payload=payload.encode('utf-8'))

    async def render_put(self, request):
        """
        TODO: paylaod_body='<state>;<display>' OPPURE (meglio) gestione da DataManager
        1) La richiesta deve contenere lo stato nel quale lo si vuole settare e anche cosa deve mostrare.
        2) DataManager, nel momento in cui leggo una modifica da plate reader invio al monitor cosa mostrare
        """
        pass

    async def render_post(self, request):
        print("EntryMonitor with ID: " + self.monitorID + " --> POST Request Received...")
        prev_state = self.monitor.state
        self.monitor.switchState()
        print("EntryMonitor with ID: " + self.monitorID + "switched state from " + prev_state + " to " + self.monitor.state)
        return aiocoap.Message(code=Code.CHANGED,
                               payload=f'{str(self.monitor.state)};display={str(self.monitor.display)}'.encode('utf-8'))
