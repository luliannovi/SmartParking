from LampBrightness import LampBrightness


class Lamp:
    """Lamp models Lamp resources used to light on the ambient
    """

    def __init__(self, brightness=0, sensorId="", description="", lampSerialized=None):
        """Constructor accepts brightness possible level.
        If lampSerialized is defined this method translates a set of json key into class variables with respective values.
        Default Lamp is OFF
        """
        self.sensorId, self.description = sensorId, description
        self.brightness = LampBrightness.LIGHT_OFF if brightness == 0 else brightness
        if lampSerialized is not None:
            self.__dict__ = lampSerialized

    def switchStatus(self):
        """This method change brightness based on current brightness.
        If above 0 it becomes 0 otherwise it becomes 1"""
        if self.brightness == 0:
            self.brightness = LampBrightness.LIGHT_LOW
        else:
            self.brightness = LampBrightness.LIGHT_OFF

    def setBrightness(self, brightness):
        """This method set a specific brightness level checking for validity.
        If an error is detected this method return False, otherwise True is returned"""
        try:
            if brightness not in [LampBrightness.__dict__.get(attribute) for attribute in LampBrightness.__dict__.keys()]:
                raise Exception()
            self.brightness = brightness
            return False
        except Exception as e:
            return False

