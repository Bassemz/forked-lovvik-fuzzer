from  scapy.layers.bluetooth4LE import *
from scapy.layers.bluetooth import *
from scapy.packet import *

OWN_MTU_Size = 23

att_layer = (
    ATT_Hdr(opcode=0x0A)/
    ATT_Read_Request(gatt_handle=79)
)
print(len(att_layer))
l2cap_layer= L2CAP_Hdr(len=len(att_layer), cid=0x0004)/att_layer
btle_data_layer = BTLE_DATA( LLID=0b10, SN=0b0, NESN=0b1, MD=0b0, RFU=0b0, len=len(l2cap_layer)) / l2cap_layer
paquet = btle_data_layer
#paquet.show()
crc  = BTLE.compute_crc(raw(paquet))
paquet.crc = int.from_bytes(crc, byteorder="little")
#paquet.show()


#paquet.show()

x = fuzz(BTLE_DATA())
x.show()