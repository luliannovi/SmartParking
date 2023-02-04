import time
import paho.mqtt.client as mqtt

from Code.Resource.PlateReader.MQTTClientParameters import MQTTClientParameters
from Code.Model.PlateReader.ParkingSensor import ParkingSensor
from Code.Logging.Logger import loggerSetup

plateLogger = loggerSetup("plateLogger_ParkingSlotSensor", "Code/Logging/Plate/plateParkingSlot.log")


class ParkingSensorResource:
    """
    The class represent the plate reader sensor of the single parking.
    """
    def __init__(self, parkingPlaceId):
        self.mqttParameters = None
        self.mqttClient = None
        self.parkingSensor = ParkingSensor(parkingPlaceId)
        self.configurations()

    def configurations(self):
        """
        Configurations for the MQTT client.
        Configurations infos retrieved from 'Configuration/PlateReaderMQTTParameters/config.json' file.
        """
        configFile = open("Configuration/PlateReaderMQTTParameters/config.json")
        self.mqttParameters = MQTTClientParameters()
        self.mqttParameters.fromJson(configFile)
        self.mqttParameters.idClient = str(self.parkingSensor.getParkingPlace())
        self.mqttParameters.LOCATION = 'parking'
        self.mqttClient = mqtt.Client(self.mqttParameters.idClient)
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.username_pw_set(self.mqttParameters.USERNAME,
                                        self.mqttParameters.PASSWORD)
        self.mqttClient.connect(self.mqttParameters.BROKER_ADDRESS,
                                self.mqttParameters.BROKER_PORT)

    def plateUpdate(self, carPlate):
        """
        Method that notify a new plate at the parking and publish, through MQTT, telemetry.
        """
        self.parkingSensor.readThePlate(carPlate)
        self.publish_telemetry()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        """
        MQTT on connection actions.
        """
        plateLogger.info("Connected with result code: " + str(rc))

    def publish_telemetry(self):
        """
        Used to share infos about a car at the exit through MQTT.
        """
        target_topic = "{0}/{1}/{2}/{3}/{4}".format(
            self.mqttParameters.BASIC_TOPIC,
            self.mqttParameters.USERNAME,
            self.mqttParameters.DEVICE_TOPIC,
            self.mqttParameters.LOCATION,
            self.mqttParameters.idClient
        )
        device_payload_string = self.parkingSensor.toJson()
        self.mqttClient.publish(target_topic, device_payload_string, 0, False)
        plateLogger.info(f"Telemetry data Published at {time.time()}: Topic: {target_topic} Payload: {device_payload_string}")
