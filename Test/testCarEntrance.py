"""
The script tests car entrance event.
"""


from Code.Model.Car.Car import Car
from Code.Model.PlateReader.EntrySensor import EntrySensor
from Code.Model.Monitor.Monitor import Monitor

from Code.Resource.PlateReader.EntrySensorResource import EntrySensorResource
from Code.Resource.CoAP.Monitor.EntryMonitor import EntryMonitor

from Code.DataHandler.DataCollector.PlateManager import PlateManager

# istanzio il plateManager, il broker MQTT che riceve i dati relativi ai parcheggi per targa letta
plateManager = PlateManager()

car = Car(licensePlate='FM056GT')
entrySensor = EntrySensor()
monitorResource = EntryMonitor(monitorID='id1', description='monitor per ingresso')

# istanza risorsa lettore targa ingresso
entrySensorResource = EntrySensorResource()
entrySensorResource.plateUpdate(car.licensePlate)

