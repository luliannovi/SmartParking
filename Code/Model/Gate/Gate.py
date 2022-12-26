import json
import time


class Gate:
    """The class models gates used in the SmartParking"""

    def __init__(self, gateID, timesleep):
        """Class have attributes:
        - state (boolean)
        - gateID (str)
        - timesleep indicates second to wait in order to close the gate after it was opened"""
        self.state = False
        self.gateID = gateID
        self.timesleep = timesleep

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
        """Switches state: closed to opened, opened to closed. If passes from closed to opened, it waits for
        self.timesleep seconds then closes it """
        if self.isOpen():
            self.closeGate()
        else:
            self.openGate()
            time.sleep(self.timesleep)
            self.closeGate()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__())
