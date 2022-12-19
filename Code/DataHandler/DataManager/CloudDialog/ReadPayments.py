import asyncio, time, json
from datetime import datetime
from Code.DataHandler.DataManager.Configuration.AzureManager import AzureManager
from Code.DataHandler.DataManager.Configuration.LocalDB import LocalDB
from Code.Model.Payment.Payment import Payment
from azure.iot.device.aio import IoTHubDeviceClient

def readMessage(message):
    """This method is used as a callback when a message from the cloud is received.
    The payment is stored inside the DB when it's read.
    If a payment is inside the DB i update it otherwise i add it.
    A payment is identified by transaction ID
    """
    try:
        data = json.loads(message.data.decode())
        messageID = message.message_id
        payment = Payment(paymentSerialized=data)
        lDB = LocalDB("PAYMENTS")
        check, flag = lDB.getPaymentByTransactionID(payment.transactionID)
        if check and flag is None:
            # add the payment
            check, flag = lDB.addPayment(payment)
            if not check:
                raise Exception(f'\terror saving data inside local DB: \n\t{flag}')
        elif check:
            # update the payment
            check, flag = lDB.updatePayment(payment)
            if not check:
                raise Exception(f'\terror saving data inside local DB: \n\t{flag}')
        else:
            #there is an error to report
            raise Exception(flag)
        print(f'message ID: {messageID}\nData: {data}\n')
    except Exception as e:
        print(f"Error reading payments from the cloud: \n{e}")

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
        print(f"Waiting for incoming messages: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        self.deviceClient.on_message_received = readMessage
        while True:
            time.sleep(1000)

# FOR TEST ONLY
# rp = ReadPayments()
# READ STATUS ONLY asyncio.run(rp.execute())






