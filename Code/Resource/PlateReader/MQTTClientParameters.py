import json


class MQTTClientParameters:
    """
    Class used to represent configuration infos of a MQTT Client.
    """
    def __init__(self):
        self.idClient = ""
        self.BROKER_ADDRESS = ""
        self.BROKER_PORT = 0
        self.USERNAME = ""
        self.PASSWORD = ""
        self.BASIC_TOPIC = ""
        self.INFO_TOPIC = ""
        self.DEVICE_TOPIC = ""
        self.LOCATION = ""

    def fromJson(self, file):
        data = json.load(file)
        self.idClient = data['idClient']
        self.BROKER_ADDRESS = data['broker_ip']
        self.BROKER_PORT = data['broker_port']
        self.USERNAME = data['username']
        self.PASSWORD = data['password']
        self.BASIC_TOPIC = data['BASIC_TOPIC']
        self.INFO_TOPIC = data['INFO_TOPIC']
        self.DEVICE_TOPIC = data['DEVICE_TOPIC']
        self.LOCATION = data['LOCATION']
