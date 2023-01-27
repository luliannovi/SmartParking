import time

from Code.DataHandler.DataManager.Configuration.LocalDB import LocalDB
from Code.Logging.Logger import loggerSetup
from Code.Model.Car.Car import Car
from Code.Model.PlateReader.EntrySensor import EntrySensor
from Code.Resource.PlateReader.EntrySensorResource import EntrySensorResource
from Code.Resource.PlateReader.ParkingSensorResource import ParkingSensorResource
from Code.Resource.PlateReader.ExitSensorResource import ExitSensorResource

car = Car(licensePlate='FM056GT')
entrySensor = EntrySensor()

# istanza risorsa lettore targa ingresso
"""entrySensorResource = EntrySensorResource()
entrySensorResource.plateUpdate(car.licensePlate)

time.sleep(10)
"""
parkingLogger = loggerSetup("parkingLogger_testCarParking","Code/Logging/Parking/parking.log")
# get first empty parking slot
lDB = LocalDB("PARKING_SLOT")
check, available, id = lDB.checkParkingSlots()
if check and available > 0:
    car = Car(licensePlate='FM056GT')
    # simulate car entrance inside parking slot inside first available slot. We suppose that par
    parkingSensorResource = ParkingSensorResource(parkingPlaceId=1)
    parkingSensorResource.plateUpdate("")
    # car leaves previous parking slot
    time.sleep(5)
    """
    time.sleep(5)
    parkingSensorResource.plateUpdate("") #uscita macchina dallo slot, update exit time
    time.sleep(5)
    """
    exitSensorResource = ExitSensorResource()
    exitSensorResource.plateUpdate("FM056GT")
else:
    parkingLogger.error("No parking slots available")
