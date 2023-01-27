import datetime
import json
import aiocoap
import paho.mqtt.client as mqtt
from Code.DataHandler.DataCollector.MQTTBrokerParameters import MQTTBrokerParameters
from Code.DataHandler.DataManager.CloudDialog.SendParkingStatus import SendParkingStatus
from Code.DataHandler.DataManager.Configuration.LocalDB import LocalDB
from Code.Model.Car.ParkingSlot import ParkingSlot
from aiocoap import *
from Code.Logging.Logger import loggerSetup

import asyncio

plateLogger = loggerSetup("plateLogger_PlateManager", "Code/Logging/Plate/plateManager.log")
sps = SendParkingStatus()

BASE_URI = 'coap://127.0.0.1:5683/'


class PlateManager:
    """This class allows to manage the incoming messages from parking considering entry/exit/parking status update.
    Incoming messages allow the following features:
        - communicate with Firebase to store online parking availabilities
        - send free slot to the entry monitor
        - update data on local json file
        - send signal to entry and exit gate
    """

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
        plateLogger.info(str(mqttBrokerParameters.idClient) + " subscribed to: " + devices_topic + "...")

    @staticmethod
    def on_message(client, userdata, msg):
        """
        Manage the arrival of a new message in:
        '..parking/in' -- manage the arrival of a new car to the entryPlateReader
        '..parking/out' -- manage the arrival of a new car to te exitPlateReader
        '..parking/id' -- manage arrival of a new car in a parking slot with a id
        """
        try:
            message_payload = str(msg.payload.decode("utf-8"))
            plateLogger.info(f"Received: Topic: {msg.topic} Payload: {message_payload} Retain: {msg.retain}")
            localParkingDBManager = LocalDB("PARKING_SLOT")
            localPaymentsDBManager = LocalDB("PAYMENTS")
            localParkedCarsDBManager = LocalDB("CAR")
            if str(msg.topic).endswith("parking/in"):
                """
                A car has arrived to the entrance
                """
                valid, availables, firstId = localParkingDBManager.checkParkingSlots()
                jsonData = json.loads(message_payload)
                if jsonData['error'] is False and valid is True:
                    asyncio.get_event_loop().run_until_complete(put_message(BASE_URI + 'monitor_in',
                                                                            "Parking slots available: " + str(
                                                                                availables) + "Nearest parking slot: " + str(
                                                                                firstId)
                                                                            + "Readed plate: " + jsonData['carPlate']))
                    asyncio.get_event_loop().run_until_complete(post_message(BASE_URI + 'IoT/actuator/gate/in'))
                    plateLogger.info(f"Arrived car with plate {jsonData['carPlate']} to the entrance.")
                elif jsonData['error'] is True:
                    asyncio.get_event_loop().run_until_complete(
                        put_message(BASE_URI + 'monitor_in', "Error in reading the plate.."
                                                             "Please press the HELP button."))
                    plateLogger.error(f"Error reading the plate of the car")
                elif valid is False:
                    asyncio.get_event_loop().run_until_complete(
                        put_message(BASE_URI + 'monitor_in', "No parking slots available. The gate will still open."))
                    asyncio.get_event_loop().run_until_complete(post_message(BASE_URI + 'IoT/actuator/gate/in'))
                    plateLogger.info(
                        f"Arrived car with plate {jsonData['carPlate']} to the entrance, but there are not available parking slots.")

            elif str(msg.topic).endswith("parking/out"):
                """
                A car has arrived to the exit
                """
                jsonData = json.loads(message_payload)
                if jsonData['error'] is True:
                    asyncio.get_event_loop().run_until_complete(
                        put_message(BASE_URI + 'IoT/device/monitor/out', "Error in reading the plate.."
                                                              "Please press the HELP button."))
                    plateLogger.error("Error reading the plate of the car.")

                else:
                    valid, instance = localPaymentsDBManager.getPaymentByLicense(jsonData['carPlate'])
                    if valid is True and instance is None:
                        asyncio.get_event_loop().run_until_complete(
                            put_message(BASE_URI + 'monitor_in', "No payments founded for your car (" + jsonData[
                                'carPlate'] + ").Please pay and comeback."))
                        plateLogger.info(
                            f"No payments founded for car with plate {jsonData['carPlate']} present at the exit gate.")
                    elif valid is True and instance is not None:
                        asyncio.get_event_loop().run_until_complete(put_message(BASE_URI + 'IoT/device/monitor/out',
                                                                                "Payments founded for your car (" +
                                                                                jsonData[
                                                                                    'carPlate'] + "). Goodbye." + instance))
                        asyncio.get_event_loop().run_until_complete(post_message(BASE_URI + 'IoT/actuator/gate/out'))
                        plateLogger.info(
                            f"Payments founded for car with plate {jsonData['carPlate']}. Sending message for gate opening.")

                        valid, value = localParkedCarsDBManager.removeParkedCar(jsonData['carPlate'])
                        if valid is False:
                            plateLogger.error(value)
                        elif value is str:
                            check, output = localPaymentsDBManager.removePaymentByLicense(jsonData['carPlate'])
                            if not check:
                                plateLogger.error(f"Error removing payment for car {jsonData['carPlate']}: {output}")
                            else:
                                plateLogger.info(value)

                    else:
                        error_string = instance
                        asyncio.get_event_loop().run_until_complete(
                            put_message(BASE_URI + 'IoT/device/monitor/out',
                                        "Error checking the payment. Please press HELP button."))
                        plateLogger.error(error_string)
            else:
                """
                A car has arrived in a parking slot
                """
                jsonData = json.loads(message_payload)

                if jsonData["car"]["licensePlate"] == "":
                    parkingSlot = ParkingSlot(jsonData['parkingPlace'],
                                              False,
                                              "")

                    valid, slot = localParkingDBManager.getParkingSlotById(givenId=jsonData['parkingPlace'])
                    if valid is False:
                        plateLogger.error(slot)
                    elif slot == []:
                        plateLogger.error(f"No parking slot founded in file while searching.")

                    else:
                        localParkingDBManager.updateParkingSlot(parkingSlot)
                        valid, value = localParkedCarsDBManager.updateExitTime(plate=slot['car'],
                                                                               exitTime=datetime.datetime.now().timestamp())
                        if valid is False:
                            plateLogger.error(value)
                        else:
                            plateLogger.info(
                                f"Updating exit time for parked car with plate {jsonData['car']['licensePlate']} in car.json file..")
                        """
                        checking parking slots available and the nearest
                        """
                        valid, availables, firstId = localParkingDBManager.checkParkingSlots()
                        if valid is True:
                            asyncio.get_event_loop().run_until_complete(put_message(BASE_URI + 'monitor_in',
                                                                                    "Total parking slots available: " + str(
                                                                                        availables) + "The nearest parking slot in: " + str(
                                                                                        firstId)))
                            plateLogger.info(
                                f"Parking slot with id: {str(parkingSlot.id)} is now free. Updating status..")
                        else:
                            error_string = availables
                            asyncio.get_event_loop().run_until_complete(
                                put_message(BASE_URI + 'IoT/device/monitor/in', error_string))
                            plateLogger.error(f"Parking slot with id: {str(parkingSlot.id)}. {str(error_string)}.")

                else:
                    """
                    A car has arrived in a parking slot
                    """
                    car = jsonData['car']
                    parkingSlot = ParkingSlot(jsonData['parkingPlace'],
                                              True,
                                              car['licensePlate'])
                    localParkingDBManager.updateParkingSlot(parkingSlot)
                    """
                    checking parking slots available and the nearest
                    """
                    valid, availables, firstId = localParkingDBManager.checkParkingSlots()
                    if valid is True:
                        asyncio.get_event_loop().run_until_complete(put_message(BASE_URI + 'IoT/device/monitor/in',
                                                                                "Total parking slots available: " + str(
                                                                                    availables) + "The nearest parking slot in: " + str(
                                                                                    firstId)))
                        plateLogger.info(
                            f"New car with plate {car['licensePlate']} in parking slot with id: {jsonData['parkingPlace']}.")
                        valid, value = localParkedCarsDBManager.insertParkedCar(plate=car['licensePlate'],
                                                                                parkingSlotID=parkingSlot.id,
                                                                                entryTime=datetime.datetime.now().timestamp(),
                                                                                exitTime=0)
                        if valid is False:
                            plateLogger.error(value)
                        else:
                            plateLogger.info(f"Writing parked car with plate {car['licensePlate']} in car.json file..")
                    else:
                        error_string = availables
                        asyncio.get_event_loop().run_until_complete(put_message(BASE_URI + 'IoT/device/monitor/in', error_string))
                        plateLogger.error(error_string)

                """Updating FireBase real-time DB"""
                plateLogger.info("Updating FireBase real-time DB...")
                check, output = localParkingDBManager.getParkingSlot()
                if check:
                    for parkingSlot in output:
                        sps.sendStatus(eval(str(parkingSlot)))

        except Exception as e:
            plateLogger.error(e)

    def stop(self):
        self.stop()


async def put_message(URI, text):
    protocol = await Context.create_client_context()
    request = Message(code=aiocoap.Code.PUT, payload=text.encode('utf-8'), uri=URI)
    try:
        response = await protocol.request(request).response
    except Exception as e:
        plateLogger.error(str(e))
    else:
        if response is not None:
            plateLogger.info('Result: %s - %r' % (response.code, response.payload.decode("utf-8")))


async def post_message(URI):
    protocol = await Context.create_client_context()
    request = Message(code=aiocoap.Code.POST, uri=URI)
    try:
        response = await protocol.request(request).response
    except Exception as e:
        plateLogger.error(str(e))
    else:
        if response is not None:
            plateLogger.info('Result: %s - %r' % (response.code, response.payload.decode("utf-8")))
