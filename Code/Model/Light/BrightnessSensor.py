import json


class BrightnessSensor:
    """BrightnessSensor models a sensor that detects AmbientBrightness"""

    def __init__(self, brightness=None, sensorId="", description=""):
        """Constructor set brightness as None either as a BrightnessSensor. If it's not None or AmbientBrightness an Exception is Raised.
        """
        self.sensorId, self.description = sensorId, description
        if isinstance(brightness, BrightnessSensor.__class__) or brightness is None:
            self.brightness = brightness
        else:
            raise Exception("Brightness must BE an Instance of BrightnessSensor/None")

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
