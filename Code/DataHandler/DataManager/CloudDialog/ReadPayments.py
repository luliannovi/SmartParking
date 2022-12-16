import os, asyncio
from Code.DataHandler.DataManager.Configuration.AzureManager import AzureManager
from azure.iot.device.aio import IoTHubDeviceClient


class ReadPayments:
    """This class allows to read incoming payments coming from cloud services
    """
    def __init__(self,type="IOTHUB"):
        """Constructor build the object that read incoming messages from Azure IoT
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

        firstConnectionString = jsonPayload.get('FIRST_CONNECTION_STRING','')
        if firstConnectionString == "":
            raise Exception("error building IoTHubDeviceClient: No connection string has been defined inside JSON config")

        self.deviceClient = IoTHubDeviceClient.create_from_connection_string(firstConnectionString)

    async def execute(self):
        """This method read all payments coming from Azure.
        receive_message() is blocking"""
        await self.deviceClient.connect()

        msg = await self.deviceClient.receive_message()
        if msg is not None:
            msgId = msg.message_id
            encoding = msg.content_encoding
            payload = msg.data.decode(encoding)

            print(msgId, encoding, payload)

rp = ReadPayments()
asyncio.run(rp.execute())




