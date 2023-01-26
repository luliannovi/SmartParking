"""
The script tests car parking event.
"""

from Code.Model.Car.Car import Car
from Code.DataHandler.DataManager.Configuration.LocalDB import LocalDB
from Code.Resource.PlateReader.ParkingSensorResource import ParkingSensorResource
from Code.Logging.Logger import loggerSetup

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
    parkingSensorResource.plateUpdate("")
    # simulate getting another place, we assume that others are empty
    parkingSensorResource = ParkingSensorResource(parkingPlaceId=6)
    parkingSensorResource.plateUpdate(car.licensePlate)
else:
    parkingLogger.error("No parking slots available")

