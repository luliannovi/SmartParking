import time

from Code.DataHandler.DataManager.Configuration.LocalDB import LocalDB
from Code.Logging.Logger import loggerSetup
from Code.Model.Car.Car import Car
from Code.Model.PlateReader.EntrySensor import EntrySensor
from Code.Resource.PlateReader.EntrySensorResource import EntrySensorResource
from Code.Resource.PlateReader.ParkingSensorResource import ParkingSensorResource

car = Car(licensePlate='FM056GT')
entrySensor = EntrySensor()

# istanza risorsa lettore targa ingresso
entrySensorResource = EntrySensorResource()
entrySensorResource.plateUpdate(car.licensePlate)

time.sleep(10)

parkingLogger = loggerSetup("parkingLogger_testCarParking","Code/Logging/Parking/parking.log")
# get first empty parking slot
lDB = LocalDB("PARKING_SLOT")
check, available, id = lDB.checkParkingSlots()
if check and available > 0:
    car = Car(licensePlate='FM056GT')
    # simulate car entrance inside parking slot inside first available slot. We suppose that par
    parkingSensorResource = ParkingSensorResource(parkingPlaceId=1)
    parkingSensorResource.plateUpdate(car.licensePlate)
    # car leaves previous parking slot
    time.sleep(10)
    parkingSensorResource.plateUpdate("")
else:
    parkingLogger.error("No parking slots available")
