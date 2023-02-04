from Code.Model.PlateReader.ExitSensor import ExitSensor
import time
import paho.mqtt.client as mqtt
from Code.Resource.PlateReader.MQTTClientParameters import MQTTClientParameters
from Code.Logging.Logger import loggerSetup

plateLogger = loggerSetup("plateLogger_ExitSensor", "Code/Logging/Plate/plateExit.log")


class ExitSensorResource:
    """
    The class represent the exit sensor of plates.
    """
    def __init__(self):
        self.mqttParameters = None
        self.mqttClient = None
        self.exitSensor = ExitSensor()
        self.configurations()

    def configurations(self):
        """
        Configurations for the MQTT client.
        Configurations infos retrieved from 'Configuration/PlateReaderMQTTParameters/config.json' file.
        """
        configFile = open("Configuration/PlateReaderMQTTParameters/config.json")
        self.mqttParameters = MQTTClientParameters()
        self.mqttParameters.fromJson(configFile)
        self.mqttParameters.idClient = 'out'
        self.mqttClient = mqtt.Client(self.mqttParameters.idClient)
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.username_pw_set(self.mqttParameters.USERNAME,
                                        self.mqttParameters.PASSWORD)
        self.mqttClient.connect(self.mqttParameters.BROKER_ADDRESS,
                                self.mqttParameters.BROKER_PORT)

    def plateUpdate(self, carPlate):
        """
        Method that notify a new plate at the exit and publish, through MQTT, telemetry.
        """
        self.exitSensor.readThePlate(carPlate)
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
        target_topic = "{0}/{1}/{2}/{3}".format(
            self.mqttParameters.BASIC_TOPIC,
            self.mqttParameters.USERNAME,
            self.mqttParameters.DEVICE_TOPIC,
            self.mqttParameters.idClient
        )
        device_payload_string = self.exitSensor.toJson()
        self.mqttClient.publish(target_topic, device_payload_string, 0, False)
        plateLogger.info(f"Telemetry data Published at {time.time()}: Topic: {target_topic} Payload: {device_payload_string}")
