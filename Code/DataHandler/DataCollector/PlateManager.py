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

plateLogger = loggerSetup("plateLogger_PlateManager", "Code/Logging/Plate/plate.log")
BASE_URI = 'coap://127.0.0.1:5683/'


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
        self.mqttClient.on_connect = PlateManager.on_connect
        self.mqttClient.on_message = PlateManager.on_message
        self.mqttClient.username_pw_set(self.mqttBrokerParameters.USERNAME,
                                        self.mqttBrokerParameters.PASSWORD)
        self.mqttClient.connect(self.mqttBrokerParameters.BROKER_ADDRESS,
                                self.mqttBrokerParameters.BROKER_PORT)
        self.mqttClient.loop_forever()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        mqttBrokerParameters = MQTTBrokerParameters()
        configparser = open('Configuration/PlateReaderMQTTParameters/config.json')
        mqttBrokerParameters.fromJson(configparser)
        devices_topic = "{0}/{1}/{2}/#".format(  # topic generico per ora
            mqttBrokerParameters.BASIC_TOPIC,
            mqttBrokerParameters.USERNAME,
            mqttBrokerParameters.DEVICE_TOPIC
        )
        client.subscribe(devices_topic)

        # print(self.mqttBrokerParameters.idClient + " subscribed to: " + devices_topic)
        plateLogger.info(mqttBrokerParameters.idClient + " subscribed to: " + devices_topic)

    @staticmethod
    def on_message(client, userdata, msg):
        try:
            message_payload = str(msg.payload.decode("utf-8"))
            plateLogger.info(f"Received: Topic: {msg.topic} Payload: {message_payload} Retain: {msg.retain}")
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
                    asyncio.get_event_loop().run_until_complete(put_message(BASE_URI + 'monitor_in',
                                                                            "Total parking slots available: " + str(
                                                                                availables) + "\nThe nearest parking slot in: " + str(
                                                                                firstId)
                                                                            + "\nReaded plate: " + jsonData['carPlate']))
                    asyncio.get_event_loop().run_until_complete(post_message(BASE_URI + 'gate_in'))

                elif jsonData['error'] is True:
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(put_message(BASE_URI + 'IoT/device/monitor/in', "Error in reading the plate.."
                                                                                            "\nPlease press the HELP button."))
                    loop.close()
                elif valid is False:
                    errorString = availables
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(put_message(BASE_URI + 'IoT/device/monitor/in', "No parking slots available."))
                    plateLogger.error(errorString)
                    loop.run_until_complete(post_message(BASE_URI + 'IoT/actuator/gate/in'))
                    loop.close()

            elif str(msg.topic).endswith("parking/out"):
                """
                control the payment
                put/post to the gate (monitor in uscita e sbarra) to open CoAP
                se non ha pagato invio al monitor messaggio d'errore 
                se sono presenti errori in lettura targa invio al monitor messaggio d'errore
                """
                jsonData = json.loads(message_payload)
                if jsonData['error'] is True:
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(put_message("uri_for_exitMonitor", "Error in reading the plate.."
                                                                               "\nPlease press the HELP button."))
                    loop.close()
                else:
                    valid, instance = localPaymentsDBManager.getPaymentByLicense(jsonData['carPlate'])
                    if valid is True and instance is None:
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(
                            put_message("uri_for _exitMonitor", "No payments founded for your car (" + jsonData[
                                'carPlate'] + "). Please pay and comeback."))
                    elif valid is True and instance is not None:
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(put_message("uri_for _exitMonitor",
                                                            "Payments founded for your car (" + jsonData[
                                                                'carPlate'] + "). Goodbye." + instance))
                        loop.run_until_complete(post_message("uri_for_exitGate"))
                    else:
                        error_string = instance
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(
                            put_message("uri_for _exitMonitor", "Error checking the payment. Please press HELP button."))
                        loop.close()
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
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(put_message("uri_entryMonitor",
                                                            "Total parking slots available: " + availables + "\nThe nearest parking slot in: " + firstId))
                        loop.close()
                    else:
                        error_string = availables
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(put_message("uri_entryMonitor", error_string))
                        loop.close()
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
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(put_message("uri_entryMonitor",
                                                            "Total parking slots available: " + availables + "\nThe nearest parking slot in: " + firstId))
                        loop.close()
                    else:
                        error_string = availables
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(put_message("uri_entryMonitor", error_string))
                        loop.close()
                        print(error_string)
        except Exception:
            pass

    def stop(self):
        self.stop()


async def put_message(URI, text):
    protocol = await Context.create_client_context()
    request = Message(code=aiocoap.Code.PUT, payload=text.encode('utf-8'), uri=URI)
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource: ')
        print(e)
    else:
        if response is not None:
            print('Result: %s\n%r' % (response.code, response.payload.decode("utf-8")))


async def post_message(URI):
    protocol = await Context.create_client_context()
    request = Message(code=aiocoap.Code.POST, uri=URI)
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource: ')
        print(e)
    else:
        if response is not None:
            print('Result: %s\n%r' % (response.code, response.payload.decode("utf-8")))
