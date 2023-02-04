import json
import time

import aiocoap
import aiocoap.resource as resource
import aiocoap.numbers as numbers
from aiocoap import Code

from kpn_senml import *

from Code.Logging.Logger import loggerSetup
from Code.Model.Monitor.Monitor import Monitor

monitorLogger = loggerSetup('monitorLogger_EntryMonitor', 'Code/Logging/Monitor/monitor.log')


class EntryMonitor(resource.Resource):
    """The class represents the resource monitor for parking entrance"""

    def __init__(self, monitorID, description):
        super().__init__()
        self.monitorID = monitorID
        self.description = description

        self.monitor = Monitor(monitorID, description)
        # interface actuator
        self.if_ = 'core.a'
        # resource type
        self.rt = 'it.resource.actuator.monitor'
        # content type
        self.ct = numbers.media_types_rev['application/senml+json']

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
        Method handles GET request.
        See method self.buildSenMLJson() in interested in payload content.
        """
        monitorLogger.info("EntryMonitor with ID: " + self.monitorID + " --> GET Request Received...")
        payload = self.buildSenMLJson()
        return aiocoap.Message(content_format=self.ct, payload=payload.encode('utf-8'))

    async def render_put(self, request):
        """
        Method handles a PUT request.
        It receives a payload containing a string that is required to be displayed on the monitor.

        See DataHandler > DataCollector > PlateManager.py if looking for message sender.
        """
        monitorLogger.info("EntryMonitor with ID: " + self.monitorID + " --> PUT Request Received...")
        json_payload_string = request.payload.decode('utf-8')
        monitorLogger.info("EntryMonitor with ID: " + self.monitorID + " --> PUT String Payload : " + json_payload_string)
        self.monitor.updateDisplay(json_payload_string)
        return aiocoap.Message(code=Code.CHANGED,
                               payload=f'{str(self.monitor.state)};display={str(self.monitor.display)}'.encode('utf-8'))

    async def render_post(self, request):
        """Method handles a POST request.
        It switches monitor state (on/off)."""
        monitorLogger.info("EntryMonitor with ID: " + self.monitorID + " --> POST Request Received...")
        self.monitor.switchState()
        return aiocoap.Message(code=Code.CHANGED,
                               payload=f'{str(self.monitor.state)};display={str(self.monitor.display)}'.encode('utf-8'))
