import json


class Monitor:
    """The class is a model for monitors inside the SmartParking"""

    def __init__(self, monitorID, description):
        """self.display indicates what the monitor is displaying (String).
        self.state indicates whether the monitor is turned on or off (boolean).
        """
        self.monitorID = monitorID
        self.description = description
        self.display = ""
        self.state = False

    def turnOn(self):
        """The method turns on the monitor: changes self.state to on."""
        self.state = True

    def turnOff(self):
        """The method turns off the monitor: changes self.state to off."""
        self.display = ""
        self.state = False

    def switchState(self):
        """The method switches the state of the monitor: on -> off and viceversa"""
        if self.state is True:
            self.turnOn()
        else:
            self.turnOff()

    def updateDisplay(self, string):
        """The method sets what the monitor displays"""
        if self.state is True:
            self.display = string
        else:
            self.turnOn()
            self.display = string

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__())
