import random
import sys

from  scapy.layers.bluetooth4LE import *
from scapy.layers.bluetooth import *
from scapy.packet import *
import json
from ctrlutils import *
from random import randbytes, randint


def readreq() :
    att_layer = (
        ATT_Hdr(opcode=0x0A)/
        ATT_Read_Request(gatt_handle=103)
    )
    l2cap_layer = L2CAP_Hdr(len=len(att_layer), cid=0x0004)/att_layer
    btle_data_layer = BTLE_DATA( LLID=0b10, SN=0b0, NESN=0b1, MD=0b0, RFU=0b0, len=len(l2cap_layer)) / l2cap_layer
    paquet = btle_data_layer
    
    crc  = BTLE.compute_crc(raw(paquet))
    paquet.crc = int.from_bytes(crc, byteorder="little")
    paquet.show()


    return paquet



def fuzzman0() :
    att_layer = (
        ATT_Hdr(opcode=0x0A)/
        ATT_Read_Request(gatt_handle=99)
    )
    l2cap_layer= L2CAP_Hdr(len=None, cid=0x0004)/att_layer
    btle_data_layer = BTLE_DATA( LLID=0b10, SN=0b0, NESN=0b1, MD=0b1, RFU=0b0, len=None) / l2cap_layer
    paquet = btle_data_layer
    crc  = BTLE.compute_crc(raw(paquet))
    paquet.crc = int.from_bytes(crc, byteorder="little")
    #paquet.show()


    return paquet


def fuzzman1() :
    x = (
        BTLE_DATA( LLID=0b10, SN=0b0, NESN=0b1, MD=0b0, RFU=0b0, len=None) /
        L2CAP_Hdr(len=None, cid=0x0004) /
        fuzz(ATT_Read_Request()) /
        fuzz(ATT_Hdr(opcode=RawVal()))
    )
    return x            

def fuzzman2() :
    x = (
        fuzz(BTLE_DATA( LLID=0b10, SN=0b0, NESN=0b1, MD=0b0, RFU=0b0, len=None)) /
        fuzz(L2CAP_Hdr()) /
        fuzz(ATT_Read_Request()) /
        fuzz(ATT_Hdr(opcode=RawVal()))
    )
    return x  
        


def fuzzwrite() :
    att_layer = (
        ATT_Hdr(opcode=0x12)/
        fuzz(ATT_Write_Request(gatt_handle=69, data=randbytes(randint(0, 10))))
    )
    l2cap_layer= L2CAP_Hdr(len=RawVal(len(att_layer)), cid=0x0004)/att_layer
    btle_data_layer = BTLE_DATA( LLID=0b10, SN=0b0, NESN=0b1, MD=0b0, RFU=0b0, len=RawVal(len(l2cap_layer))) / l2cap_layer
    paquet = btle_data_layer
    crc  = BTLE.compute_crc(raw(paquet))
    paquet.crc = int.from_bytes(crc, byteorder="little")
    paquet.show()

    return paquet




def mtureq() :
    att_layer = (
        ATT_Hdr(opcode=0x02)/
        ATT_Exchange_MTU_Request(mtu=OWN_MTU_Size)
    )
    print(len(att_layer))
    l2cap_layer= L2CAP_Hdr(len=len(att_layer), cid=0x0004)/att_layer
    btle_data_layer = BTLE_DATA( LLID=0b10, SN=0b0, NESN=0b1, MD=0b0, RFU=0b0, len=len(l2cap_layer)) / l2cap_layer
    mtupaquet = btle_data_layer
    mtupaquet.show()
    crc  = BTLE.compute_crc(raw(mtupaquet))
    mtupaquet.crc = int.from_bytes(crc, byteorder="little")
    print(type(crc))
    mtupaquet.show()

    return mtupaquet



def use_random_packet_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    #Picked random
    key = "ATT_Exchange_MTU_Request"
    ATT_layer_packet_class = globals()[key]
    arguments = {}
    for k,v in data[key]["arguments"].items():
        if not len(v["range"]) >1:
            print("Error tried to generate a packet with unsupported value generation")
            sys.exit(0)
        arguments[k] = random.randint(v["range"][0], v["range"][1])
    ATT_Layer_packet = ATT_layer_packet_class(**arguments)
    packet = fill_packet(int(data[key]["opcode"],16) ,ATT_Layer_packet)
    return packet

def fill_packet(opcode, ATT_Layer_packet):
    att_layer = (
            ATT_Hdr(opcode=opcode)/
            ATT_Layer_packet
    )
    l2cap_layer = L2CAP_Hdr(len=len(att_layer), cid=0x0004)/att_layer
    btle_data_layer = BTLE_DATA( LLID=0b10, SN=0b0, NESN=0b1, MD=0b0, RFU=0b0, len=len(l2cap_layer)) / l2cap_layer
    paquet = btle_data_layer

    crc  = BTLE.compute_crc(raw(paquet))
    paquet.crc = int.from_bytes(crc, byteorder="little")
    paquet.show()
    return paquet

if __name__ == "__main__":
    # Use the json file outputted from the element
    use_random_packet_from_json("results/att_request_pdus_remapped_latest.json")