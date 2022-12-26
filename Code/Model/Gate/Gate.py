import json


class Gate:
    """The class models gates used in the SmartParking"""

    def __init__(self, gateID):
        """Class only have 2 attribute: state (boolean) gateID (str).
        If it's set to True """
        self.state = False
        self.gateID = gateID

    def openGate(self):
        """The method opens the gate: sets self.state to True"""
        self.state = True

    def closeGate(self):
        """The method closes the gate: sets self.state to False"""
        self.state = False

    def isOpen(self):
        """Returns True if gate is opened"""
        return self.state is True

    def isClosed(self):
        """Returns True if gate is closed"""
        return self.state is False

    def switchState(self):
        """Switches state: closed to opened, opened to closed"""
        if self.isOpen():
            self.closeGate()
        else:
            self.openGate()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__())
