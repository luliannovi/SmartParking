import json
import logging
import time
import aiocoap
import paho.mqtt.client as mqtt
from Code.DataHandler.DataCollector.MQTTBrokerParameters import MQTTBrokerParameters
from Code.DataHandler.DataManager.Configuration.LocalDB import LocalDB
from Code.Model.Car.ParkingSlot import ParkingSlot
from aiocoap import *
from Code.Logging.Logger import loggerSetup

import asyncio

plateLogger = loggerSetup("plateLogger","Code/Logging/Plate/plate.log")

class PlateManager:
    """This class allows to manage the incoming messages from parking considering entry/exit/parking status update.
    Incoming messages allow the following features:
        - communicate with Firebase to store online parking availabilities
        - send free slot to the entry monitor"""

    def __init__(self):
        self.mqttClient = None
        self.mqttBrokerParameters = None
        self.configurations()

    def configurations(self):
        self.mqttBrokerParameters = MQTTBrokerParameters()
        configparser = open('Configuration/PlateReaderMQTTParameters/config.json')
        self.mqttBrokerParameters.fromJson(configparser)
        self.mqttBrokerParameters.idClient = "PlateManager"
        self.mqttClient = mqtt.Client(self.mqttBrokerParameters.idClient)
        self.mqttClient.on_connect = lambda client, userdata, flags, rc: self.on_connect(client, userdata, flags, rc)
        self.mqttClient.on_message = lambda client, userdata, msg: self.on_message(client, userdata, msg)
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

        #print(self.mqttBrokerParameters.idClient + " subscribed to: " + devices_topic)
        plateLogger.info(self.mqttBrokerParameters.idClient + " subscribed to: " + devices_topic)

    @staticmethod
    def on_message(self, client, userdata, msg):
        message_payload = str(msg.payload.decode("utf-8"))
        print(f"Received IoT Message at {time.time().__str__()}:\nTopic: {msg.topic}\nPayload: {message_payload}")
        localParkingDBManager = LocalDB("PARKING_SLOT")
        localPaymentsDBManager = LocalDB("PAYMENTS")
        if str(msg.topic).endswith("parking/in"):
            """
            no update to json files, if a car does not park it does not pay
            put/post to the gate (risorsa monitor in entrata e sbarra entrata) to open CoAP
            se sono presenti errori in lettura targa invio al monitor messaggio d'errore
            """
            valid, availables, firstId = localParkingDBManager.checkParkingSlots()

            jsonData = json.loads(message_payload)

            if jsonData['error'] is False and valid is True:
                self.put_message("uri_for_entryMonitor",
                            "Total parking slots available: " + availables + "\nThe nearest parking slot in: " + firstId
                            + "\nReaded plate: " + jsonData['carPlate'])
                self.post_message("uri_for_gate")
            elif jsonData['error'] is True:
                self.put_message("uri_for_entryMonitor", "Error in reading the plate.."
                                                    "\nPlease press the HELP button.")
            elif valid is False:
                errorString = availables
                self.put_message("uri_for_entryMonitor", "No parking slots available.")
                print(errorString)
                self.post_message("uri_for_gate")

        elif str(msg.topic).endswith("parking/out"):
            """
            control the payment
            put/post to the gate (monitor in uscita e sbarra) to open CoAP
            se non ha pagato invio al monitor messaggio d'errore 
            se sono presenti errori in lettura targa invio al monitor messaggio d'errore
            """
            jsonData = json.loads(message_payload)
            if jsonData['error'] is True:
                self.put_message("uri_for_exitMonitor", "Error in reading the plate.."
                                                   "\nPlease press the HELP button.")
            else:
                valid, instance = localPaymentsDBManager.getPaymentByLicense(jsonData['carPlate'])
                if valid is True and instance is None:
                    self.put_message("uri_for _exitMonitor", "No payments founded for your car (" + jsonData[
                        'carPlate'] + "). Please pay and comeback.")
                elif valid is True and instance is not None:
                    self.put_message("uri_for _exitMonitor",
                                "Payments founded for your car (" + jsonData['carPlate'] + "). Goodbye." + instance)
                    self.post_message("uri_for_exitGate")
                else:
                    error_string = instance
                    self.put_message("uri_for _exitMonitor", "Error checking the payment. Please press HELP button.")
                    print(error_string)
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
                valid, availables, firstId = localParkingDBManager.checkParkingSlots()
                if valid is True:
                    self.put_message("uri_entryMonitor",
                                "Total parking slots available: " + availables + "\nThe nearest parking slot in: " + firstId)
                else:
                    error_string = availables
                    self.put_message("uri_entryMonitor", error_string)
                    print(error_string)

            else:
                car = jsonData['car']
                parkingSlot = ParkingSlot(jsonData['parkingPlace'],
                                          True,
                                          car.licensePlate)
                localParkingDBManager.addParkingSlot(parkingSlot)
                """
                checking parking slots available and the nearest
                """
                valid, availables, firstId = localParkingDBManager.checkParkingSlots()
                if valid is True:
                    self.put_message("uri_entryMonitor",
                                "Total parking slots available: " + availables + "\nThe nearest parking slot in: " + firstId)
                else:
                    error_string = availables
                    self.put_message("uri_entryMonitor", error_string)
                    print(error_string)

    def stop(self):
        self.stop()

    @staticmethod
    async def put_message(self, URI, text):
        logging.basicConfig(level=logging.INFO)
        protocol = await Context.create_client_context()
        request = Message(code=aiocoap.Code.PUT, payload=text, uri=URI)
        try:
            response = await protocol.request(request).response
        except Exception as e:
            print(print('Failed to fetch resource: '))
            print(e)
        else:
            print('Result: %s\n%r' % (response.code, response.payload))

    @staticmethod
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


