import json
import time
from Code.Logging.Logger import loggerSetup


gateLogger = loggerSetup('gateLogger_Gate', 'Code/Logging/Gate/gate.log')

class Gate:
    """The class models gates used in the SmartParking"""

    def __init__(self, gateID, description, timesleep):
        """Class have attributes:
        - state (boolean)
        - gateID (str)
        - description (str)
        - timesleep (int indicating seconds) indicates second to wait in order to close the gate after it was opened"""
        self.state = False
        self.gateID = gateID
        self.timesleep = timesleep
        self.description = description

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
            gateLogger.info(f"Gate state: {'OPEN' if self.state else 'CLOSED'}")
            self.closeGate()
            gateLogger.info(f"Gate state: {'OPEN' if self.state else 'CLOSED'}")
        else:
            gateLogger.info(f"Gate state: {'OPEN' if self.state else 'CLOSED'}")
            self.openGate()
            gateLogger.info(f"Gate state: {'OPEN' if self.state else 'CLOSED'}")
            time.sleep(self.timesleep)
            self.closeGate()
            gateLogger.info(f"Gate state: {'OPEN' if self.state else 'CLOSED'}")

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
