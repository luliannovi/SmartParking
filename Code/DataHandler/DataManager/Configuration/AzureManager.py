import json
from Code.Model.Payment import Payment


class AzureManager:
    """This class defines methods required to store/read/update data inside configuration file.
    We should reset each night payament.json, anyway..."""

    SUPPORTED_MEDIA = {"AZURE":"Configuration/AzureHubIoT/azure.json",
                       "IOTHUB":"Configuration/AzureHubIoT/IoTHub.json"}

    def __init__(self,type):
        """type is the media that we want to handle calling the class.
        Calling the constructor i check if the media type is supported.
        """
        if type not in AzureManager.SUPPORTED_MEDIA:
            raise Exception("Requested media type is not supported")
        else:
            self.type = type

    """Methods to handle azure credentials"""
    def getJsonData(self):
        """This method return AZURE credentials
        True,jsonData is returned if everything is ok otherwise False,STR is returned.
        """
        try:
            with open(AzureManager.SUPPORTED_MEDIA[self.type], "r") as jsonStream:
                dataJson = json.load(jsonStream)
            return True, dataJson
        except Exception as e:
            return False, f'Error with "getJsonData": {e}'

