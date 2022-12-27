import json


class Monitor:
    """The class is a model for monitors inside the SmartParking"""

    def __init__(self):
        """self.display indicates what the monitor is displaying (String).
        self.state indicates whether the monitor is turned on or off (boolean).
        """
        self.display = ""
        self.state = False

    def turnOn(self):
        """The method turns on the monitor: changes self.state to on."""
        self.state = True

    def turnOff(self):
        """The method turns off the monitor: changes self.state to off."""
        self.display = ""
        self.state = False

    def updateDisplay(self, string):
        """The method sets what the monitor displays"""
        if self.state is True:
            self.display = string
        else:
            raise ValueError("Unable to update display: monitor is off.")

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__())
