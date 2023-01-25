import time
import aiocoap
import aiocoap.resource as resource
import aiocoap.numbers as numbers
from aiocoap import Code
from kpn_senml import *
from Code.Logging.Logger import loggerSetup
from Code.Model.Gate.Gate import Gate

gateLogger = loggerSetup('gateLogger_EntryGate', 'Code/Logging/Gate/gate.log')

class EntryGate(resource.Resource):
    """
    The class represents the resource Gate for park's entrance
    """

    def __init__(self, gateID, description, timesleep):
        """
        @param timesleep: indicates second to wait in order to close the gate after it was opened
        """
        super().__init__()
        self.gateID = gateID
        self.timesleep = timesleep
        self.description = description

        self.entryGate = Gate(self.gateID, description, timesleep)
        # interface actuator
        self.if_ = "core.a"
        # resource type
        self.rt = "it.resource.actuator.gate"
        # content type
        self.ct = numbers.media_types_rev['application/senml+json']

    def buildSenMLJson(self):
        """The method created a SenML+Json representation of the gate resource."""
        state = self.entryGate.state
        pack = SenmlPack(self.gateID)
        gate = SenmlRecord("EntryGate",
                           unit="bool",  # no standard unit exists
                           value=state,
                           time=int(time.time()))
        pack.add(gate)
        return pack.to_json()

    async def render_get(self, request):
        """Method handles GET requests"""
        gateLogger.info("EntryGate with ID: " + self.gateID + " --> GET Request Received...")
        payload = self.buildSenMLJson()
        return aiocoap.Message(content_format=self.ct, payload=payload.encode('utf-8'))

    async def render_post(self, request):
        """Method handles POST requests. Changes Gate state"""
        gateLogger.info("EntryGate with ID: " + self.gateID + " --> POST Request Received...")
        self.entryGate.switchState()
        return aiocoap.Message(code=Code.CHANGED,
                               payload=f'{str(self.entryGate.state)};timesleep={str(self.timesleep)}'.encode('utf-8'))
