import logging, asyncio, aiocoap.resource as resource, aiocoap
from Code.Resource.CoAP.Monitor.EntryMonitor import EntryMonitor
from Code.Resource.CoAP.Monitor.ExitMonitor import ExitMonitor
from Code.Resource.CoAP.Gate.EntryGate import EntryGate
from Code.Resource.CoAP.Gate.ExitGate import ExitGate
from Code.Resource.CoAP.Light.LampResource import LampResource
from Code.Logging.Logger import loggerSetup

gateLogger = loggerSetup('gateLogger_CoAPserver', 'Code/Logging/Gate/gate.log')

def main():
    # Resource tree creation
    root = resource.Site()

    # Add WellKnownCore Resource to support the standard Resource Discovery
    root.add_resource(['.well-known', 'core'],
                      resource.WKCResource(root.get_resources_as_linkheader, impl_info=None))

    # define ids
    root.add_resource(['IoT', 'device', 'monitor', 'in'], EntryMonitor(monitorID='id1', description='entry monitor'))
    root.add_resource(['IoT', 'device', 'monitor', 'out'], ExitMonitor(monitorID='id2', description='exit monitor'))
    root.add_resource(['IoT', 'actuator', 'gate', 'in'], EntryGate(gateID='id3', description='entry gate', timesleep=10))
    root.add_resource(['IoT', 'actuator', 'gate', 'out'], ExitGate(gateID='id4', description='exit gate', timesleep=10))
    # add all light sensor
    for index in range(1,11):
        root.add_resource(['IoT', 'actuator', 'lamp', str(index)], LampResource(sensorId=f'id{index}', description="parking slot generic lamp"))




    asyncio.Task(aiocoap.Context.create_server_context(root, bind=('127.0.0.1', 5683)))
    gateLogger.info(f'CoAP server started...')
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    main()
