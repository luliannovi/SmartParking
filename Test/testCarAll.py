"""
The script tests car parking event.
"""

from Code.Model.Car.Car import Car
from Code.DataHandler.DataManager.Configuration.LocalDB import LocalDB
from Code.Resource.PlateReader.ParkingSensorResource import ParkingSensorResource
from Code.Resource.PlateReader.ExitSensorResource import ExitSensorResource
from Code.Resource.PlateReader.EntrySensorResource import EntrySensorResource
from Code.Logging.Logger import loggerSetup

parkingLogger = loggerSetup("parkingLogger_testCarParking","Code/Logging/Parking/parking.log")
# get first empty parking slot
lDB = LocalDB("PARKING_SLOT")
check, available, id = lDB.checkParkingSlots()
if check and available > 0:
    car = Car(licensePlate='FM056GT')

    entrySensor = EntrySensorResource()
    entrySensor.plateUpdate(car.licensePlate)
    # simulate car entrance inside parking slot inside first available slot. We suppose that par
    parkingSensorResource1 = ParkingSensorResource(parkingPlaceId=1)
    parkingSensorResource1.plateUpdate(car.licensePlate)
    # car leaves previous parking slot
    parkingSensorResource1.plateUpdate("")

    parkingSensorResource2 = ParkingSensorResource(parkingPlaceId=2)
    parkingSensorResource2.plateUpdate(car.licensePlate)

    parkingSensorResource2.plateUpdate("")

    exitSensor = ExitSensorResource()
    exitSensor.plateUpdate(car.licensePlate)
else:
    parkingLogger.error("No parking slots available")
