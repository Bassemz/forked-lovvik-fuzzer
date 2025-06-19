from whad.ble.connector.central import Central

from whad import UartDevice
from whad.ble.exceptions import *
from time import sleep

from trafficlog import TrafficLogger
from discovery import *
from ctrlutils import *
from packetforge import *


TARGET_BD_ADDR = "44:17:93:5E:39:82"

central = Central(UartDevice("/dev/ttyACM0"))
tl = TrafficLogger(central)


try :
    target = central.connect(TARGET_BD_ADDR, timeout=10)
except Exception as e:
    tl.toggle()
    tl.finish()
    print(f"connection failed {e}")
    exit(-1)

'''try :
    target.discover()
except :
    tl.toggle()
    tl.finish()
    print("discovery err")
    exit(-1)'''

'''for service in target.services():
    print(f'-- Service {service.name}')
    for charac in service.characteristics():
        print(f' + Characteristic {charac.name} Handle {charac.handle} {showProperties(charac)}')
#print(central.export_profile())'''


#target.read(79)
#target.read(82)
#target.read(85)


pkt = readreq()
#xpkt = fuzzreadreq()


time.sleep(0.5)
'''print("sending packets wait...")
for i in range(3) :    
    central.send_pdu(pkt)
    time.sleep(0.1)'''


print("fuzzing ongoing...")   
start = time.time()
try :
    while True :
        central.send_pdu(use_random_packet_from_json("results/att_request_pdus_remapped_latest.json"))
        time.sleep(0.1)
        break
        #central.send_pdu(fuzzman2())
        
except KeyboardInterrupt :
    pass
except ConnectionLostException :
    print("Err : connection lost")
    pass
print(f"duration : {time.time()-start} s")




"""#wait for response, Ctrl+C to stop
print("> Loop started (CTRL+C)...")
try:
    while True:
        continue
except KeyboardInterrupt:
    pass
"""

target.disconnect()

tl.finish()
