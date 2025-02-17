import time

from aiocoap import Code
import aiocoap.resource as resource
import aiocoap.numbers as numbers
import aiocoap

from kpn_senml import *

from Code.Logging.Logger import loggerSetup
from Code.Model.Gate.Gate import Gate


gateLogger = loggerSetup('gateLogger_ExitGate', 'Code/Logging/Gate/gate.log')


class ExitGate(resource.Resource):
    """
    The class represents the resource Gate for park's exit
    """

    def __init__(self, gateID, description, timesleep):
        """
        @param gateID: ID of the exit gate (str)
        @param description: gate description (str)
        @param timesleep: seconds the gate has to wait before
        automatically closing after it was opened (int indicating seconds)
        """
        super().__init__()
        self.gateID = gateID
        self.description = description
        self.timesleep = timesleep

        self.exitGate = Gate(gateID, description, timesleep)
        # interface actuator
        self.if_ = 'core.a'
        # resource type
        self.rt = 'it.resource.actuator.gate'
        # content type
        self.ct = numbers.media_types_rev['application/senml+json']

    def buildSenMLJson(self):
        """The method creates a senml+json representation of the resource exit gate"""
        state = self.exitGate.state
        pack = SenmlPack(self.gateID)
        gate = SenmlRecord("ExitGate",
                           unit="bool",  # no standard unit exists
                           value=state,
                           time=int(time.time()))

        pack.add(gate)
        return pack.to_json()

    async def render_get(self, request):
        """Method handles GET requests"""
        gateLogger.info("ExitGate with ID: " + self.gateID + " --> GET Request Received...")
        payload = self.buildSenMLJson()
        return aiocoap.Message(content_format=self.ct, payload=payload.encode('utf-8'))

    async def render_post(self, request):
        """Method handles POST requests. Changes Gate state"""
        gateLogger.info("ExitGate with ID: " + self.gateID + " --> POST Request Received...")
        self.exitGate.switchState()
        return aiocoap.Message(code=Code.CHANGED,
                               payload=f'{str(self.exitGate.state)};timesleep={str(self.timesleep)}'.encode('utf-8'))
