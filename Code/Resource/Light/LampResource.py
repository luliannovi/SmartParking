import json
import aiocoap.resource as resource
import aiocoap
from aiocoap.numbers.codes import Code
from Code.Model.Light.Lamp import Lamp
from Code.Model.Light.LampBrightness import LampBrightness


class LampResource(resource.Resource):
    """
    Scheletro di risorsa, in questo caso per LampResource

    Ditemi se è corretta che la riproduco per altri oggetti

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

    async def render_get(self, request):
        print("LampResource with ID: " + self.lightEmittor.sensorId + " --> GET Request Received ...")
        payload_string = json.dumps(self.lightEmittor)
        return aiocoap.Message(content_format=50, payload=payload_string.encode('utf8'))

    async def render_put(self, request):
        print("LampResource with ID: " + self.lightEmittor.sensorId + " --> PUT Request Received ...")
        json_payload_string = request.payload.decode('UTF-8')
        print(
            "LampResource with ID: " + self.lightEmittor.sensorId + " --> PUT String Payload : %s" % json_payload_string)

        """
        Ricevo oggetto Lamp con brightness già impostata come desiderata
        in base ad essa vado poi a modificare la brightness di lightEmittor, attributo di questo oggetto LightResource
        """
        lampReceived = Lamp(**json.loads(json_payload_string))
        if lampReceived.brightness == LampBrightness.LIGHT_OFF:
            self.lightEmittor.switchStatus()
            self.update_state()
            return aiocoap.Message(code=Code.CHANGED)

        """
        Qui effettuo i vari controlli possibili su luminosità d'emissione luce ricevuta
        """
