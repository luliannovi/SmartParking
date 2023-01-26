"""This file orchestrate MQTT & CoAP server"""
import os, sys, atexit
from subprocess import Popen
p = Popen([sys.executable,"./Test/CoAPserver.py"])
p1 = Popen([sys.executable,"./Test/RunPlateManager.py"])
p2 = Popen([sys.executable,"./Test/RunLightManager.py"])


def closeAllProcess():
    p.terminate()
    p1.terminate()
    p2.terminate()

atexit.register(closeAllProcess)


while(1):
    continue