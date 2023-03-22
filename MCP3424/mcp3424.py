"""Driver for MCP3424 ADC.
"""
import busio

ADDRESS = 0x68


class MCP3424:
    BIT_MAP = { # Bit rate choices
        12: 0b00,
        14: 0b01,
        16: 0b10,
        18: 0b11,
    }

    CHANNEL_MAP = { # Channel choices
        0: 0b00,
        1: 0b01,
        2: 0b10,
        3: 0b11,
    }

    GAIN_MAP = { # Gain choices
        1: 0b00,
        2: 0b01,
        4: 0b10,
        8: 0b11,
    }

    def __init__(self, i2c_bus: busio.I2C, bits=18, channel=1, gain=1):
        """Initialize the driver.

        Args:
            i2c_bus (busio.I2C): I2C bus where the ADC is located
            bits (int, optional): Bit rate. Defaults to 18.
            channel (int, optional): Channel to read. Defaults to 1.
            gain (int, optional): Gain of the signal. Defaults to 1.
        """
        self.bits = bits
        self.channel = channel
        self.gain = gain
        self._i2c = i2c_bus

        self.setup()

    @property
    def bits(self):
        return self._bits
    
    @bits.setter
    def bits(self, bits):
        if bits not in self.BIT_MAP:
            raise ValueError(f"{bits} is not a valid bit rate")
        self._bits = bits

    @property
    def channel(self):
        return self._channel
    
    @channel.setter
    def channel(self, channel):
        if channel not in self.CHANNEL_MAP:
            raise ValueError(f"{channel} is not a valid channel")
        self._channel = channel

    @property
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, gain):
        if gain not in self.GAIN_MAP:
            raise ValueError(f"{gain} is not a valid gain")
        self._gain = gain

    def setup(self):
        # Write the desired bit rate, channel and gain to the device.
        while not self._i2c.try_lock():
            pass

        self._i2c.writeto(
            ADDRESS,
            bytes(
                [0b1<<7|self.CHANNEL_MAP[self._channel]<<5|
                0b1<<4|self.BIT_MAP[self._bits]<<2|self.GAIN_MAP[self._gain]]
            )
        )

    def read(self):
        if self._bits > 15:
            result = bytearray(3)
        else:
            result = bytearray(2)
        
        self._i2c.readfrom_into(ADDRESS, result)

        if self._bits == 18:
            number = (result[0]&0b1)<<16|result[1]<<8|result[2]
            if result[0]&0b10==1:
                number = -1*number
            number = number*15.625
        elif self._bits == 16:
            number = (result[0]&0b1111111)<<8|result[1]

            if result[0]&0b10000000==1:
                number = -1*number
            number = number*62.5
        elif self._bits == 14:
            number = (result[0]&0b11111)<<8|result[1]

            if (result[0]&0b100000)==1:
                number = -1*number
            number = number*250
        elif self._bits == 12:
            number = (result[0]&0b111)<<8|result[1]

            if result[0]&0b1000==1:
                number = -1*number
            number = number*1000
        number = number*self._gain
        return number
