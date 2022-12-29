from Code.Model.PlateReader.EntrySensor import EntrySensor
import time
import paho.mqtt.client as mqtt

from MQTTClientParameters import MQTTClientParameters
import json


class ParkingSensorResource:

    def __init__(self):
        self.mqttParameters = None
        self.mqttClient = None
        self.entrySensor = EntrySensor()
        self.configurations()

    def configurations(self):
        configFile = open("Configuration/PlateReaderMQTTParameters/config.json")
        self.mqttParameters = MQTTClientParameters()
        self.mqttParameters.fromJson(configFile)
        self.mqttParameters.idClient = "in"
        self.mqttParameters.LOCATION = 'parking'
        self.mqttClient = mqtt.Client(self.mqttParameters.idClient)
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.username_pw_set(self.mqttParameters.USERNAME,
                                        self.mqttParameters.PASSWORD)
        self.mqttClient.connect(self.mqttParameters.BROKER_ADDRESS,
                                self.mqttParameters.BROKER_PORT)

    def plateUpdate(self, carPlate):
        self.entrySensor.carPlate = carPlate
        self.publish_telemetry()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code: " + str(rc))

    def publish_telemetry(self):
        target_topic = "{0}/{1}/{2}/{3}/{4}".format(
            self.mqttParameters.BASIC_TOPIC,
            self.mqttParameters.USERNAME,
            self.mqttParameters.DEVICE_TOPIC,
            self.mqttParameters.LOCATION,
            self.mqttParameters.idClient
        )
        device_payload_string = self.entrySensor.toJson()
        self.mqttClient.publish(target_topic, device_payload_string, 0, True)
        print(f"Telemetry data Published at {time.time()}: \nTopic: {target_topic}\nPayload: {device_payload_string}")
