import json
import aiocoap.resource as resource
import aiocoap
from aiocoap.numbers.codes import Code
from Code.Model.Light.Lamp import Lamp
from Code.Model.Light.LampBrightness import LampBrightness
from Code.Logging.Logger import loggerSetup

lampLogger = loggerSetup("plateLogger_lampResource", "Code/Logging/Light/light.log")


class LampResource(resource.Resource):
    """
    Scheletro di risorsa, in questo caso per LampResource

    Controllate:
    - nomi attributi
    - messaggi riccevuti-inviati
    - correttezza serializzazione-deserializzazione
    """

    def __init__(self, brightness=0, sensorId="", description="", lampSerialized=None):
        super().__init__()
        self.lightEmittor = Lamp()
        if brightness != 0:
            self.lightEmittor.brightness = brightness
        if sensorId != "":
            self.lightEmittor.sensorId = sensorId
        if description != "":
            self.lightEmittor.description = description
        if lampSerialized is not None:
            self.__dict__ = lampSerialized
        # interface actuator
        self.if_ = "core.a"
        # resource type
        self.rt = "it.resource.actuator.lamp"

    async def render_get(self, request):
        lampLogger.info("LampResource with ID: " + self.lightEmittor.sensorId + " --> GET Request Received ...")
        payload_string = json.dumps(self.lightEmittor)
        return aiocoap.Message(content_format=50, payload=payload_string.encode('utf8'))

    async def render_put(self, request):
        """
        Receive a Lamp object with the correct brightness, setup the right brightness in lightEmittor.
        """
        lampLogger.info("LampResource with ID: " + self.lightEmittor.sensorId + " --> PUT Request Received ...")
        json_payload_string = request.payload.decode('UTF-8')
        lampLogger.info(
            "LampResource with ID: " + self.lightEmittor.sensorId + " --> PUT String Payload : %s" % json_payload_string)

        lampReceived = Lamp(**json.loads(json_payload_string))
        if lampReceived.brightness == LampBrightness.LIGHT_OFF:
            self.lightEmittor.switchStatus()
            lampLogger.info(f"Switched brightness from {LampBrightness.LIGHT_OFF} to {self.lightEmittor.brightness}")
            return aiocoap.Message(code=Code.CHANGED)
        else:
            lampLogger.info(f"Switched brightness from {self.lightEmittor.brightness} to {lampReceived.brightness}")
            self.lightEmittor.setBrightness(lampReceived.brightness)
            return aiocoap.Message(code=Code.CHANGED)

    async def render_post(self):
        """
        Receive a request to change the status.
        """
        lampLogger.info("LampResource with ID: " + self.lightEmittor.sensorId + " --> POST Request Received ...")
        self.lightEmittor.switchStatus()
        lampLogger.info(f"Switched brightness to {self.lightEmittor.brightness}")
        return aiocoap.Message(code=Code.CHANGED)
