import json

import aiocoap
import asyncio
import link_header
import paho.mqtt.client as mqtt
from Code.DataHandler.DataCollector.MQTTBrokerParameters import MQTTBrokerParameters
from Code.Model.Light.LampBrightness import LampBrightness
from aiocoap import *
from Code.Logging.Logger import loggerSetup


lightLogger = loggerSetup("lightLogger_LightManager", "Code/Logging/Light/light.log")
BASE_URI = 'coap://127.0.0.1:5683/'


class LightManager:
    """This class allows to manage the incoming messages from the only light sensor available considering emitted light.
    Incoming messages allow the following features:
        - regulate all the available lamp
    """

    def __init__(self):
        self.mqttClient = None
        self.mqttBrokerParameters = None
        self.configurations()

    def configurations(self):
        self.mqttBrokerParameters = MQTTBrokerParameters()
        configparser = open('Configuration/BrightnessSensorMQTTParameters/config.json')
        self.mqttBrokerParameters.fromJson(configparser)
        self.mqttBrokerParameters.idClient = "LightManager"
        self.mqttClient = mqtt.Client(self.mqttBrokerParameters.idClient)
        self.mqttClient.on_connect = LightManager.on_connect
        self.mqttClient.on_message = LightManager.on_message
        self.mqttClient.username_pw_set(self.mqttBrokerParameters.USERNAME,
                                        self.mqttBrokerParameters.PASSWORD)
        self.mqttClient.connect(self.mqttBrokerParameters.BROKER_ADDRESS,
                                self.mqttBrokerParameters.BROKER_PORT)
        self.mqttClient.loop_forever()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        mqttBrokerParameters = MQTTBrokerParameters()
        configparser = open('Configuration/BrightnessSensorMQTTParameters/config.json')
        mqttBrokerParameters.fromJson(configparser)
        devices_topic = "{0}/{1}/{2}".format(  # topic generico per ora
            mqttBrokerParameters.BASIC_TOPIC,
            mqttBrokerParameters.USERNAME,
            mqttBrokerParameters.DEVICE_TOPIC
        )
        client.subscribe(devices_topic)
        lightLogger.info(str(mqttBrokerParameters.idClient) + " subscribed to: " + devices_topic + "...")

    @staticmethod
    def on_message(client, userdata, msg):
        """
        Manage the arrival of a new message in sensor/light
        """
        try:
            message_payload = int(json.loads(str(msg.payload.decode("utf-8")))["brightness"])
            lightLogger.info(f"Received: Topic: {msg.topic} Payload: {message_payload} Retain: {msg.retain}")
            valoreRegolazione = LampBrightness.calculateBrightnessFromLumen(message_payload)
            asyncio.get_event_loop().run_until_complete(updateAllLamp(BASE_URI, valoreRegolazione))

        except Exception as e:
            lightLogger.error(e)

    def stop(self):
        self.stop()


async def put_message(URI, text):
    protocol = await Context.create_client_context()
    request = Message(code=aiocoap.Code.PUT, payload=text.encode('utf-8'), uri=URI)
    try:
        response = await protocol.request(request).response
    except Exception as e:
        lightLogger.error(str(e))
    else:
        if response is not None:
            lightLogger.info('Result: %s - %r' % (response.code, response.payload.decode("utf-8")))

async def post_message(URI):
    protocol = await Context.create_client_context()
    request = Message(code=aiocoap.Code.POST, uri=URI)
    try:
        response = await protocol.request(request).response
    except Exception as e:
        lightLogger.error(str(e))
    else:
        if response is not None:
            lightLogger.info('Result: %s - %r' % (response.code, response.payload.decode("utf-8")))

async def updateAllLamp(BASE_URI, BRIGHTNESS_LEVEL):
    # scarico con il resource discovery tutti i lampioni
    protocol = await Context.create_client_context()
    request = Message(code=Code.GET, uri=BASE_URI+".well-known/core")
    try:
        response = await protocol.request(request).response
    except Exception as e:
        lightLogger.error(str(e))
    else:
        if response is not None:
            response_string = response.payload.decode("utf-8")
            links_headers = link_header.parse(response_string)
            # printing response
            for link in links_headers.links:
                if len(link.attr_pairs) > 1 and link.attr_pairs[1][1]=="it.resource.actuator.lamp":
                    URI = link.href[1:]
                    request = Message(code=aiocoap.Code.PUT, payload=str(BRIGHTNESS_LEVEL).encode('utf-8'), uri=BASE_URI+URI)
                    try:
                        response = await protocol.request(request).response
                    except Exception as e:
                        lightLogger.error(str(e))
                    else:
                        if response is not None:
                            lightLogger.info('Attuation with result: %s' % (response.code))



