import json
import time
import aiocoap
import paho.mqtt.client as mqtt
from MQTTBrokerParameters import MQTTBrokerParameters
from Code.DataHandler.DataManager.Configuration.LocalDB import LocalDB
from Code.Model.Car.ParkingSlot import ParkingSlot
from aiocoap import *
from Code.Logging.Logger import loggerSetup




class PlateManager:
    """This class allows to manage the incoming messages from parking considering entry/exit/parking status update.
    Incoming messages allow the following features:
        - communicate with Firebase to store online parking availabilities
        - send free slot to the entry monitor"""

    def __init__(self):
        self.mqttClient = None
        self.mqttBrokerParameters = None

    def configurations(self):
        self.mqttBrokerParameters = MQTTBrokerParameters()
        configparser = open('Configuration/PlateReaderMQTTParameters/config.json')
        self.mqttBrokerParameters.fromJson(configparser)
        self.mqttBrokerParameters.idClient = "PlateManager"
        self.mqttClient = mqtt.Client(self.mqttBrokerParameters.idClient)
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_message = self.on_message
        self.mqttClient.username_pw_set(self.mqttBrokerParameters.USERNAME,
                                        self.mqttBrokerParameters.PASSWORD)
        self.mqttClient.connect(self.mqttBrokerParameters.BROKER_ADDRESS,
                                self.mqttBrokerParameters.BROKER_PORT)
        self.mqttClient.loop_forever()

    @staticmethod
    def on_connect(self, client, userdata, flags, rc):
        devices_topic = "{0}/{1}/{2}/{3}/#".format(  # topic generico per ora
            self.mqttBrokerParameters.BASIC_TOPIC,
            self.mqttBrokerParameters.USERNAME,
            self.mqttBrokerParameters.DEVICE_TOPIC,
            self.mqttBrokerParameters.LOCATION
        )
        self.mqttClient.subscribe(devices_topic)

        print(self.mqttBrokerParameters.idClient + " subscribed to: " + devices_topic)

    @staticmethod
    def on_message(client, userdata, message):
        message_payload = str(message.payload.decode("utf-8"))
        print(f"Received IoT Message at {time.time().__str__()}:\nTopic: {message.topic}\nPayload: {message_payload}")
        localParkingDBManager = LocalDB("PARKING_SLOT")
        localPaymentsDBManager = LocalDB("PAYMENTS")
        if str(message.topic).endswith("parking/in"):
            """
            no update to json files, if a car does not park it does not pay
            put/post to the gate (risorsa monitor in entrata e sbarra entrata) to open CoAP
            se sono presenti errori in lettura targa invio al monitor messaggio d'errore
            """
            ret = localParkingDBManager.checkParkingSlots()

            jsonData = json.loads(message_payload)

            if jsonData['error'] is False and ret[0] is True:
                put_message("uri_for_entryMonitor",
                            "Total parking slots available: " + ret[1] + "\nThe nearest parking slot in: " + ret[2]
                            + "\nReaded plate: " + jsonData['carPlate'])
                post_message("uri_for_gate")
            elif jsonData['error'] is True:
                put_message("uri_for_entryMonitor", "Error in reading the plate.."
                                                    "\nPlease press the HELP button.")
            elif ret[0] is False:
                put_message("uri_for_entryMonitor", "No parking slots available.")
                print(ret[1])
                post_message("uri_for_gate")

        elif str(message.topic).endswith("parking/out"):
            """
            control the payment
            put/post to the gate (monitor in uscita e sbarra) to open CoAP
            se non ha pagato invio al monitor messaggio d'errore 
            se sono presenti errori in lettura targa invio al monitor messaggio d'errore
            """
            jsonData = json.loads(message_payload)
            if jsonData['error'] is True:
                put_message("uri_for_exitMonitor", "Error in reading the plate.."
                                                   "\nPlease press the HELP button.")
            else:
                ret = localPaymentsDBManager.getPaymentByLicense(jsonData['carPlate'])
                if ret[0] is True and ret[1] is None:
                    put_message("uri_for _exitMonitor", "No payments founded for your car (" + jsonData[
                        'carPlate'] + "). Please pay and comeback.")
                elif ret[0] is True and ret[1] is not None:
                    put_message("uri_for _exitMonitor",
                                "Payments founded for your car (" + jsonData['carPlate'] + "). Goodbye." + ret[1])
                    post_message("uri_for_exitGate")
                else:
                    put_message("uri_for _exitMonitor", "Error checking the payment. Please press HELP button.")
                    print(ret[1])
        else:
            """
            TODO: put/post to the monitor parking slots free and the nearest place
                    reading from the json
            """
            jsonData = json.loads(message_payload)
            if jsonData['car'] is None:
                parkingSlot = ParkingSlot(jsonData['parkingPlace'],
                                          False,
                                          "")
                localParkingDBManager.addParkingSlot(parkingSlot)
                """
                checking parking slots available and the nearest
                """
                ret = localParkingDBManager.checkParkingSlots()
                if ret[0] is True:
                    put_message("uri_entryMonitor",
                                "Total parking slots available: " + ret[1] + "\nThe nearest parking slot in: " + ret[2])
                else:
                    put_message("uri_entryMonitor", ret[1])
                    print(ret[1])

            else:
                car = jsonData['car']
                parkingSlot = ParkingSlot(jsonData['parkingPlace'],
                                          True,
                                          car.licensePlate)
                localParkingDBManager.addParkingSlot(parkingSlot)
                """
                checking parking slots available and the nearest
                """
                ret = localParkingDBManager.checkParkingSlots()
                if ret[0] is True:
                    put_message("uri_entryMonitor",
                                "Total parking slots available: " + ret[1] + "\nThe nearest parking slot in: " + ret[2])
                else:
                    put_message("uri_entryMonitor", ret[1])
                    print(ret[1])

    def loop(self):
        self.configurations()

    def stop(self):
        self.stop()


async def put_message(URI, message):
    logging.basicConfig(level=logging.INFO)
    protocol = await Context.create_client_context()
    request = Message(code=aiocoap.Code.PUT, payload=message, uri=URI)
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print(print('Failed to fetch resource: '))
        print(e)
    else:
        print('Result: %s\n%r' % (response.code, response.payload))


async def post_message(URI):
    logging.basicConfig(level=logging.INFO)
    protocol = await Context.create_client_context()
    request = Message(code=aiocoap.Code.POST, uri=URI)

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print(print('Failed to fetch resource: '))
        print(e)
    else:
        print('Result: %s\n%r' % (response.code, response.payload))
