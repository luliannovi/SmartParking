from Code.DataHandler.DataManager.Configuration.AzureManager import AzureManager
from azure.iot.device.aio import IoTHubDeviceClient



class SendParkingStatus:
    """This class allows to send all'parking status
    """

    class SendParkingStatus:
        """This class allows to read incoming payments coming from cloud services
        """

        def __init__(self, type="PARKING_SLOT"):
            """Constructor build the object that send data to Azure IoT
            """
            self.type = type
            self.buildConnection(self.type)

        def buildConnection(self, type):
            """buildConnection use to create an instance of IoTHubDeviceClient from json file values
            """
            azureManager = AzureManager(type)
            check, jsonPayload = azureManager.getJsonData()
            if not check:
                raise Exception(jsonPayload)

            firstConnectionString = jsonPayload.get('FIRST_CONNECTION_STRING', '')
            if firstConnectionString == "":
                raise Exception(
                    "error building IoTHubDeviceClient: No connection string has been defined inside JSON config")

            self.deviceClient = IoTHubDeviceClient.create_from_connection_string(firstConnectionString, websockets=True)

        def send(self, payload):
            """Payload is expected to be a serialized json"""
            self.deviceClient.send_message(payload)
            # TODO -> end implementation with specific headers

