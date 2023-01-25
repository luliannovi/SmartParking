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
    parkingSensorResource = ParkingSensorResource(parkingPlace=id)
    parkingSensorResource.plateUpdate(car.licensePlate)
    # TODO -> FARE L'USCITA DAL POSTO DI PARCHEGGIO

    # TODO -> FARE CAMBIO POSTO IN PARCHEGGIO
else:
    parkingLogger.error("No parking slots available")

