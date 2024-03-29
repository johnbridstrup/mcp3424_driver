"""
Test script for reading data from an MCP3424 Analog-to-Digital converter behind a
TCA9548a multiplexer board.
"""
import time
import board
import busio
import adafruit_tca9548a
from MCP3424.mcp3424 import MCP3424

i2c = busio.I2C(board.SCL, board.SDA)
mux = adafruit_tca9548a.TCA9548A(i2c, address=0x70) # Change the address as needed

bits = 18 # 18, 16, 14, 12
channel = 0 # 0, 1, 2, 3
gain = 1 # 1, 2, 4, 8
 
mcp = MCP3424(mux[1], bits, channel, gain) # use i2c instead of mux[1] if going directly into the ADC and not using the multiplexer

while True:

    data = mcp.read()
    print("{:+,.2f} uV".format(data))
    print("{:+.5f} mV".format(data/1000))
    print("{:+.7f} V".format(data/1000000))
    time.sleep(1)