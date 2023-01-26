from Code.Model.Light.BrightnessSensor import BrightnessSensor
import time
import paho.mqtt.client as mqtt
from Code.Resource.Light.MQTTClientParameters import MQTTClientParameters
from Code.Logging.Logger import loggerSetup

brightnessSensorLogger = loggerSetup("plateLogger_BrightnessSensor", "Code/Logging/Light/light.log")


class BrightnessSensorResource:
    def __init__(self, brightness=None, sensorId="", description=""):
        self.mqttParameters = None
        self.mqttClient = None
        self.brightnessSensor = BrightnessSensor(brightness, sensorId, description)
        self.configurations()

    def configurations(self):
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
        self.brightnessSensor.brightness = brightness
        self.publish_telemetry()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        brightnessSensorLogger.info("Connected with result code: " + str(rc))

    def publish_telemetry(self):
        """
        Used to share info about brightness in the parking through MQTT.
        It sends an entire BrightnessSensor object.
        """
        target_topic = "{0}/{1}/{2}/{3}".format(
            self.mqttParameters.BASIC_TOPIC,
            self.mqttParameters.USERNAME,
            self.mqttParameters.DEVICE_TOPIC,
            self.mqttParameters.idClient
        )
        device_payload_string = self.brightnessSensor.toJson()
        self.mqttClient.publish(target_topic, device_payload_string, 0, False)
        brightnessSensorLogger.info(
            f"Telemetry data Published at {time.time()}: Topic: {target_topic}Payload: {device_payload_string}")
