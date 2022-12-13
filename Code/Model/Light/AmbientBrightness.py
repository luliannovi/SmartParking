class AmbientBrightness:
    """This class models Ambient Brightness using Lumen unit of measure"""
    ACCEPTED_MIN = 0
    ACCEPTED_MAX = 10000

    def __init__(self, brightness=0, ambientbrightnessSerialized=None):
        """Brightness accepted values are inside this range -> [ACCEPTED_MIN, ACCEPTED_MAX].
        Brightness is casted to integer
        """
        self.brightness = int(brightness) if brightness >= AmbientBrightness.ACCEPTED_MIN and brightness <= AmbientBrightness.ACCEPTED_MAX else 0
        if ambientbrightnessSerialized is not None:
            self.__dict__ = ambientbrightnessSerialized

    def setBrightness(self, brightness=0):
        """This method checks for brightness values before setting it.
        If brightness is uncorrect its set as 0"""
        self.brightness = int(brightness) if brightness >= AmbientBrightness.ACCEPTED_MIN and brightness <= AmbientBrightness.ACCEPTED_MAX else 0

