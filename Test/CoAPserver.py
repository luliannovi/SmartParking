import logging, asyncio, aiocoap.resource as resource, aiocoap
from Code.Resource.CoAP.Monitor.EntryMonitor import EntryMonitor
from Code.Resource.CoAP.Monitor.ExitMonitor import ExitMonitor
from Code.Resource.CoAP.Gate.EntryGate import EntryGate
from Code.Resource.CoAP.Gate.ExitGate import ExitGate
from Code.Logging.Logger import loggerSetup

gateLogger = loggerSetup('gateLogger_CoAPserver', 'Code/Logging/Gate/gate.log')

def main():
    # Resource tree creation
    root = resource.Site()
    # define ids
    root.add_resource(['monitor_in'], EntryMonitor(monitorID='id1', description='entry monitor'))
    root.add_resource(['monitor_out'], ExitMonitor(monitorID='id2', description='exit monitor'))
    root.add_resource(['gate_in'], EntryGate(gateID='id3', description='entry gate', timesleep=10))
    root.add_resource(['gate_out'], ExitGate(gateID='id4', description='exit gate', timesleep=10))

    # Add WellKnownCore Resource to support the standard Resource Discovery
    asyncio.Task(aiocoap.Context.create_server_context(root, bind=('127.0.0.1', 5683)))
    gateLogger.info(f'CoAP server started...')
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    main()