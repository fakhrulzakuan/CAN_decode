#!/usr/bin/env python

""" ARS408 ROS Driver
# Python 2.7
# Author : Fakhrul Zakuan
# Email : fakhrulzakuan@gmail.com
"""
import can

class MotionInput:

    def __init__(self):

        self.bus = can.Bus(interface='socketcan',
            bustype='socketcan_ctypes',
            channel= 'vcan0',
            bitrate="500000",
            receive_own_messages=True)

        #The bit order for BIG ENDIAN
        ################################################################################
        #|       Byte 0     |          Byte 1        | ... |            Byte 7        |#
        #|bit7 6 5 4 3 2 1 0|bit15 14 13 12 11 10 9 8| ... |bit63 62 61 60 59 58 57 56|#
        ################################################################################

        #The bit order for LITTLE ENDIAN
        ##################################################################################
        #|           Byte 7         |          Byte 6          | ... |       Byte 0     |#
        #|bit63 62 61 60 59 58 57 56|bit55 54 53 52 51 50 49 48| ... |bit7 6 5 4 3 2 1 0|#
        ##################################################################################

        #Speed Direction
        #BIG ENDIAN
        #CAN ID: 0x200
        #Start bit: bit6 with 2 bits length. 
        #Unit: 0 = Standtill, 1 = Forward, 2 = backward

        ######################
        #|       Byte 0     |#   
        #|bit7 6            |#
        ######################

        #Speed
        #BIG ENDIAN
        #CAN ID: 0x200
        #Start bit: bit8 with 13 bits length.
        #Resolution: 0.02 
        #Min: 0.0
        #Max: 163.8 
        #Unit: m/s

        ###############################################
        #|       Byte 0     |          Byte 1        |#
        #|         4 3 2 1 0|bit15 14 13 12 11 10 9 8|#
        ###############################################

        #Yaw Rate
        #BIG ENDIAN
        #CAN ID: 0x200
        #Start bit: bit24 with 16 bits length.
        #Resolution: 0.01 
        #Offset: -327.67
        #Min: -327.67
        #Max: +327.67
        #Unit: m/s

        #####################################################################################################
        #|       Byte 0     |          Byte 1        |          Byte 2          |          Byte 3          |#
        #|                  |                        |bit23 22 21 20 19 18 17 16|bit31 30 29 28 27 26 25 24|#
        #####################################################################################################

        #Sample Data
        speed = 1.0
        yawrate = 0.0

        self.SendMotionInput(speed, yawrate)

    def SendMotionInput(self, speed, yawrate):

        #Create an empty variable to hold 64 bits
        dec_as_bit = bin(0)[2:].zfill(64)

        if speed > 0.0:
            direction = 1

        elif speed == 0.0:
            direction = 0

        else:
            direction = 2

        #Encode the value as bit data
        dec_speed = int(round((speed / 0.02) , 2))
        dec_yawrate = int(round(((yawrate + 327.67) / 0.01) , 2))


        #Insert the bit data and shift them to its position according to the start bit
        dec_as_bit = bin(direction << 62 | 
                        dec_speed << 48 |
                        dec_yawrate << 32)[2:].zfill(64)     

        #Convert the bit as byte then convert as decimal.

        #BIG ENDIAN 
        bit_as_byte = [int(dec_as_bit[0:8],2),
                        int(dec_as_bit[8:16],2),
                        int(dec_as_bit[16:24],2),
                        int(dec_as_bit[24:32],2),
                        int(dec_as_bit[32:40],2),
                        int(dec_as_bit[40:48],2),
                        int(dec_as_bit[48:56],2),
                        int(dec_as_bit[56:64],2)]

        #LITTLE ENDIAN
        # bit_as_byte =  bit_as_byte[::-1]

        #Transmit the data to CAN. 
        transmit_data = can.Message(arbitration_id=512, data=bit_as_byte, extended_id=False)
        self.bus.send(transmit_data)

        print transmit_data

if __name__ == '__main__':
 
    _MotionInput = MotionInput()