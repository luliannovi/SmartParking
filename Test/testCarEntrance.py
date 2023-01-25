"""
The script tests car entrance event.
"""

from Code.Model.Car.Car import Car
from Code.Model.PlateReader.EntrySensor import EntrySensor
from Code.Resource.PlateReader.EntrySensorResource import EntrySensorResource


car = Car(licensePlate='FM056GT')
entrySensor = EntrySensor()

# istanza risorsa lettore targa ingresso
entrySensorResource = EntrySensorResource()
entrySensorResource.plateUpdate(car.licensePlate)
