import time
import board
import busio
import adafruit_tca9548a
from MCP3424.mcp3424 import MCP3424

i2c = busio.I2C(board.SCL, board.SDA)
mux = adafruit_tca9548a.TCA9548A(i2c, address=0x70) # Change the address as needed

bits = 18 # 18, 16, 14, 12
channels = [0, 1] # 0, 1, 2, 3
gain = 1 # 1, 2, 4, 8
 
mcp = MCP3424(mux[1], bits, channels[0], gain) # use i2c instead of mux[1] if going directly into the ADC and not using the multiplexer

while True:
    for channel in channels:
        data = mcp.read_from_channel(channel, delay=True)
        print(f"Channel {channel} uV:", "{:+,.2f}".format(data))
        print(f"Channel {channel} mV:", "{:+.5f}".format(data/1000))
        print(f"Channel {channel} V:", "{:+.7f}".format(data/1000000))
    time.sleep(1)