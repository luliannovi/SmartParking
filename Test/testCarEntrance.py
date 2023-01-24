"""
The script tests car entrance event.
"""

from Code.Model.Car.Car import Car
from Code.Model.PlateReader.EntrySensor import EntrySensor
from Code.Model.Monitor.Monitor import Monitor

from Code.Resource.PlateReader.EntrySensorResource import EntrySensorResource
from Code.Resource.CoAP.Monitor.EntryMonitor import EntryMonitor

from Code.DataHandler.DataCollector.PlateManager import PlateManager

car = Car(licensePlate='FM056GT')
entrySensor = EntrySensor()

# istanza risorsa lettore targa ingresso
entrySensorResource = EntrySensorResource()
entrySensorResource.plateUpdate(car.licensePlate)
