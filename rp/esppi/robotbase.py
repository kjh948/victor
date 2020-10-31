# -*- coding: utf-8 -*-

import serial
import struct
import sys
import time
import math
import numpy as np
import logging

logger = logging.getLogger("robotbase")

try:
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
except:
    pass
    
def serialWriteNumToByte(token, var=[]): # Only to be used for c m u b i l o within Python
    #print("Num Token "); print(token);print(" var ");print(var);print("\n\n");
    if token =='c' or token =='m' or token =='u' or token =='b':
        instrStr = token + ":" + str(var[0])+","+str(var[1])+'\n'
    logger.info("robot command send: "+ instrStr)
    ser.write(instrStr.encode())

if __name__ == '__main__':
    while 1:
        serialWriteNumToByte('m',[10000,0])
        time.sleep(0.1)
        serialWriteNumToByte('m',[0,0])
        time.sleep(0.1)
        serialWriteNumToByte('m',[0,10000])
        time.sleep(0.1)