"""This file orchestrate MQTT & CoAP server"""
import sys, atexit
from subprocess import Popen

fileList = ["./Code/Logging/Light/light.log", "./Code/Logging/DB/db.log", "./Code/Logging/Gate/gate.log",
            "./Code/Logging/Monitor/monitor.log", "./Code/Logging/Parking/parking.log", "./Code/Logging/Payments/payments.log",
            "./Code/Logging/Plate/plateEntry.log", "./Code/Logging/Plate/plateExit.log", "./Code/Logging/Plate/plateManager.log",
            "./Code/Logging/Plate/plateParkingSlot.log"]
for file in fileList:
    f = open(file,"w")
    f.close()

p = Popen([sys.executable, "./Test/CoAPserver.py"])
p1 = Popen([sys.executable, "./Test/RunPlateManager.py"])
p2 = Popen([sys.executable, "./Test/RunLightManager.py"])


def closeAllProcess():
    p.terminate()
    p1.terminate()
    p2.terminate()


atexit.register(closeAllProcess)

while (1):
    continue
