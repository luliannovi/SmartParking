import json
import time
import paho.mqtt.client as mqtt
from MQTTBrokerParameters import MQTTBrokerParameters
from Code.DataHandler.DataManager.Configuration.LocalDB import LocalDB
from Code.Model.Car.ParkingSlot import ParkingSlot
from Code.Model.Car.Car import Car


class PlateManager:
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
        localDBManager = LocalDB("PARKING_SLOT")
        if str(message.topic).endswith("parking/in"):
            """
            send data to the manager that manage entry plates
            """
        elif str(message.topic).endswith("parking/out"):
            """
            send data to the manager that manage exit plates
            """
        else:
            jsonData = json.loads(message_payload)
            if isinstance(jsonData, list):
                parkingSlot = ParkingSlot(jsonData.pop(0),
                                          False,
                                          [])
                localDBManager.addParkingSlot(parkingSlot)
            else:
                car = jsonData['car']
                parkingSlot = ParkingSlot(jsonData['parkingPlace'],
                                          True,
                                          [{"licensePlate": car.licensePlate, "entryTime": car.entryTime}])
                localDBManager.addParkingSlot(parkingSlot)

    def loop(self):
        self.configurations()

    def stop(self):
        self.stop()
