#!/usr/bin/env python

""" CAN DECODE
# Python 2.7
# Author : Fakhrul Zakuan
# Email : fakhrulzakuan@gmail.com
"""

import can, binascii
import sys
print sys.byteorder

class DecodeCAN:

    def __init__(self):

        self.bus = can.Bus(interface='socketcan',
            bustype='socketcan_ctypes',
            channel= 'vcan0',
            bitrate="500000",
            receive_own_messages=True)

        self.can_callback() 

    def can_callback(self):

        while True:
            try:
                
                # The can_msg.data is in a bytearray format
                # where byte 0 (first byte) starts from left. By default this is BIG ENDIAN.
                # In order to convert it to LITTLE ENDIAN, all you have to do is put invert syntax [::-1]
                # binascii.hexlify is just one way to convert bytearray in hex format. 
                # You can also use 'format' or 'struct' but I've tested and binascii is 3 times faster.

                can_msg = self.bus.recv()

                self.can_ID = hex(can_msg.arbitration_id)[2:] 
                can_as_byte_big = binascii.hexlify(can_msg.data)
                can_as_byte_little = binascii.hexlify(can_msg.data[::-1])
                self.can_as_bit = bin(int(can_as_byte_little, 16))[2:].zfill(64)[::-1]

                # self.can_as_bit = ''.join(format(ord(byte), '08b') for byte in can_msg.data).zfill(64)
                
                #Now this is where it gets confusing for most people, the bit order. 
                #The bit0 is always start from the first bit of Byte0, then bit8 is the first bit of Byte1.
                #So the bit order for BIG ENDIAN will looks like this. 

                ################################################################################
                #|       Byte 0     |          Byte 1        | ... |            Byte 7        |#
                #|bit7 6 5 4 3 2 1 0|bit15 14 13 12 11 10 9 8| ... |bit63 62 61 60 59 58 57 56|#
                ################################################################################

                #On the other hand, the bit order for LITTLE ENDIAN will be like this. 

                ##################################################################################
                #|           Byte 7         |          Byte 6          | ... |       Byte 0     |#
                #|bit63 62 61 60 59 58 57 56|bit55 54 53 52 51 50 49 48| ... |bit7 6 5 4 3 2 1 0|#
                ##################################################################################

                #Let's say you want to call bit 0 in BIG ENDIAN format. It is located at index 7 in self.can_as_bit.
                #self.can_as_bit[7]  = "bit 0"
                #self.can_as_bit[6]  = "bit 1"
                #self.can_as_bit[5]  = "bit 2"
                #self.can_as_bit[63] = "bit 56"

                print can_as_byte_big, can_as_byte_little

                self.ReadCAN(self.can_as_bit)
               
            except KeyboardInterrupt:
                print("Program Exited")
                break
            except can.CanError:
                print("Message NOT sent")
                break
    
    def ReadCAN(self, binaryraw):

        #Example: You want to decode Speed data. 
        #BIG ENDIAN
        #CAN ID is 0x201
        #Start bit is at bit8 with 13 bits length. 
        #The resolution is 0.02 m/s

        #Therefore, the only bits we need to extract is |bit4 3 2 1 0 |bit15 14 13 12 11 10 9 8|

        if self.can_ID == "201":

            bit_speed = binaryraw[3:16]
            decimal_speed = int(bit_speed, 2)
            data_speed = round((decimal_speed * 0.02) , 2)
            print "Speed: ", data_speed, "m/s"

        
        #Example: You want to decode Distance data. 
        #LITTLE ENDIAN
        #CAN ID is 0x201
        #Start bit is at bit8 with 13 bits length. 
        #The resolution is 0.02 m
        #The offset is 

        #Therefore, the only bits we need to extract is |bit60 59 58 57 56|bit55 54 53 52 51 50 49 48|
            
        elif self.can_ID == "203":
          
            bit_distance = binaryraw[3:16]
            decimal_distance = int(bit_distance, 2)
            data_distance = round((decimal_distance * 0.02) , 2)
            print "Distance: ", data_distance, "m"
        
        else:
            pass
    

if __name__ == "__main__":

    _DecodeCAN = DecodeCAN()

    
    

