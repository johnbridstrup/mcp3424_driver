# This file runs the code for the MCP3422 sensor
import board
import busio
import adafruit_tca9548a

i2c = busio.I2C(board.SCL, board.SDA)
mux = adafruit_tca9548a.TCA9548A(i2c, address=0x70)

ADDRESS = 0x68

class MCP3424:
    def __init__(self, bits, channel, gains):
        self.bits = bits
        self.channel = channel
        self.gains = gains
#init object with defaults.
mcp = MCP3424(18,1,1)

def setup(bits,channel,gains):
    mcp.bits = bits
    mcp.channel = channel
    mcp.gains = gains
    bit_array={12:0b00,14:0b01,16:0b10,18:0b11} # Sample rate map
    channel_array={1:0b00,2:0b01}
    gain_array = {1:0b00,2:0b01,4:0b10,8:0b11} 
    while not mux[1].try_lock():
        pass
    print(mux[1].scan())
    print(bin(0b1<<7|channel_array[channel]<<5|
                0b1<<4|bit_array[bits]<<2|gain_array[gains]))
    mux[1].writeto(ADDRESS,bytes([0b1<<7|channel_array[channel]<<5|
                0b1<<4|bit_array[bits]<<2|gain_array[gains]]))

# returns the data in microvolts
def read():
    bits = mcp.bits
    gains = mcp.gains
    number = 0
    if bits>15:
        result = bytearray(3)
    else:
        result = bytearray(2)
    mux[1].readfrom_into(ADDRESS,result)
    
    if bits == 18:
        number = (result[0]&0b1)<<16|result[1]<<8|result[2]
        if result[0]&0b10==1:
            number = -1*number
        number = number*15.625
    elif bits == 16:
        number = (result[0]&0b1111111)<<8|result[1]

        if result[0]&0b10000000==1:
            number = -1*number
        number = number*62.5
    elif bits == 14:
        number = (result[0]&0b11111)<<8|result[1]

        if (result[0]&0b100000)==1:
            number = -1*number
        number = number*250
    elif bits == 12:
        number = (result[0]&0b111)<<8|result[1]

        if result[0]&0b1000==1:
            number = -1*number
        number = number*1000
    number = number*gains
    return number