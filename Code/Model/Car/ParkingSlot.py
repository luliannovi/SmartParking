import json
from Code.Model.Car.Car import Car


class ParkingSlot:
    """This class defines a parking slot, it's used to deserialize local DB.

    Parking Slot structure:
    {
        "id":1,
        "state": "True", -> as a string, check for eval(...)
        "car":[
            {
                "licensePlate":"...",
                "entryTime":timestamp
            }
        ]
    }"""

    def __init__(self, id = 0, state = False, car = None, parkingslotSerialized=None):
        """Constructor method, by default, set id as 0 and empty parking slot.
        If state is True a Car must be set.
        A proper car is stored inside the json file."""
        self. id = id
        self.state = state
        self.car = car

        if parkingslotSerialized is not None:
            self.parkingSlotDeserializer(parkingslotSerialized)


    def parkingSlotDeserializer(self, parkingslotSerialized):
        """This method deserialize a dictionary containing an instance of a parking slot.
        1) I build parkingSlot instance
        2) If state is True i check for car instance and i build it
        """
        self.id =  int(parkingslotSerialized.get("id", "")) if parkingslotSerialized.get("id", "") != "" else 999
        self.state = eval(parkingslotSerialized.get("state", "False"))
        if self.state is True:
            self.car = Car(licensePlate=parkingslotSerialized.get("car", ""))
        else:
            self.car = None

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__())

    def __repr__(self):
        return json.dumps({"parkingId" : self.id,
                "state" : str(self.state),
                "car" : self.car.licensePlate if self.car is not None else ""
                })

