from Code.Model.Light.BrightnessSensor import BrightnessSensor
import time
import paho.mqtt.client as mqtt
from Code.Resource.Light.MQTTClientParameters import MQTTClientParameters
from Code.Logging.Logger import loggerSetup

brightnessSensorLogger = loggerSetup("plateLogger_BrightnessSensor", "Code/Logging/Light/light.log")


class BrightnessSensorResource:
    """
    The class represents the brightness sensor's resources.
    """
    def __init__(self, brightness=None, sensorId="", description=""):
        self.mqttParameters = None
        self.mqttClient = None
        self.brightnessSensor = BrightnessSensor(brightness, sensorId, description)
        self.configurations()

    def configurations(self):
        """
        Configurations for the MQTT client.
        Configurations infos retrieved from 'Configuration/BrightnessSensorMQTTParameters/config.json' file.
        """
        configFile = open("Configuration/BrightnessSensorMQTTParameters/config.json")
        self.mqttParameters = MQTTClientParameters()
        self.mqttParameters.fromJson(configFile)
        self.mqttParameters.idClient = self.brightnessSensor.sensorId
        self.mqttParameters.LOCATION = ''
        self.mqttClient = mqtt.Client(self.mqttParameters.idClient)
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.username_pw_set(self.mqttParameters.USERNAME,
                                        self.mqttParameters.PASSWORD)
        self.mqttClient.connect(self.mqttParameters.BROKER_ADDRESS,
                                self.mqttParameters.BROKER_PORT)

    def brightnessUpdate(self, brightness):
        """
        Method that notify a new brightness in the environment and publish, through MQTT, telemetry.
        """
        self.brightnessSensor.brightness = brightness
        self.publish_telemetry()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        """
        MQTT on connection actions.
        """
        brightnessSensorLogger.info("Connected with result code: " + str(rc))

    def publish_telemetry(self):
        """
        Method used to share infos about brightness in the parking through MQTT.
        It sends an entire BrightnessSensor object.
        Used in 'brightnessUpdate()' method.
        """
        target_topic = "{0}/{1}/{2}".format(
            self.mqttParameters.BASIC_TOPIC,
            self.mqttParameters.USERNAME,
            self.mqttParameters.DEVICE_TOPIC
        )
        device_payload_string = self.brightnessSensor.toJson()
        self.mqttClient.publish(target_topic, device_payload_string, 0, False)
        brightnessSensorLogger.info(
            f"Telemetry data Published at {time.time()}: Topic: {target_topic} Payload: {device_payload_string}")
