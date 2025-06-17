#placeholder value
ATT_MTU = 0

## ATT Payload size range : 0 to (ATT_MTU - X)
# X = 1 if Authentication Signature Flag of the Attribute Opcode is 0
# X = 13 if Authentication Signature Flag of the Attribute Opcode is 1 

ATT_PL_Size = ATT_MTU - 1

# range (23 - Inf)
OWN_MTU_Size = 23


## T_IFS
# minimum amount of time to wait before sending another packet (after a T or a R)
# t_IFS = 150 us
T_IFS =  150e-6
WAIT_TIME = 15e-2