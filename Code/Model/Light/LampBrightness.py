from Code.Model.Light.AmbientBrightness import AmbientBrightness

class LampBrightness:
    """LampBrightness defines the levels accepted to regulate Lamp resource"""
    LIGHT_OFF = 0
    LIGHT_LOW = 1
    LIGHT_SEMI_LOW = 2
    LIGHT_MEDIUM = 3
    LIGHT_HIGH = 4
    LIGHT_MAX = 5

    @staticmethod
    def calculateBrightnessFromLumen(lumen):
        ranges = [0,0,0,0,0,0]
        division = AmbientBrightness.ACCEPTED_MAX/6
        for index in range(0,5):
            ranges[index] = division if index == 0 else ranges[index-1]+division

        for index in len(ranges):
            if lumen < ranges[index]:
                return index

        return LampBrightness.LIGHT_OFF

