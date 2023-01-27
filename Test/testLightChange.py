from Code.Resource.Light.BrightnessSensorResource import BrightnessSensorResource
import random, time

# send lumen received from sensor to LightManager
# lumen sensor possible range [0,2000]
while True:
    brightnessSensorResource = BrightnessSensorResource(sensorId="id", description="description")
    brightnessSensorResource.brightnessUpdate(random.randrange(0, 2000, 10))
    time.sleep(30)
