"""Driver for MCP3424 ADC.
"""
import busio
import time

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

    def __init__(self, i2c_bus: busio.I2C, bits=18, channel=1, gain=1, max_lock_retries=10, lock_retry_delay=0.25):
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
        self.max_lock_retries = max_lock_retries
        self.lock_retry_delay = lock_retry_delay

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

    def _try_lock(self):
        counter = 0
        while not self._i2c.try_lock():
            counter += 1
            if counter >= self.max_lock_retries:
                raise RuntimeError(
                    (f"Could not acquire I2C lock. Retried {counter} times in "
                    f"{self.max_lock_retries*self.lock_retry_delay} seconds.")
                )
            time.sleep(self.lock_retry_delay)

    def _write_to(self, channel):
        if channel != self.channel:
            self.channel = channel
        
        self._i2c.writeto(
            ADDRESS,
            bytes(
                [0b1<<7|self.CHANNEL_MAP[self._channel]<<5|
                0b1<<4|self.BIT_MAP[self._bits]<<2|self.GAIN_MAP[self._gain]]
            )
        )

    def setup(self):
        # Attempt to acquire the lock
        self._try_lock()

        # Write to initial channel selection
        self._write_to(self.channel)

    def _get_result_bytes(self):
        if self._bits > 15:
            return bytearray(3)
        else:
            return bytearray(2)

    def _get_voltage(self, result):
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

        return number*self._gain

    def read(self):
        """Continuously read from currently set channel

        Returns:
            float: Voltage in uV
        """
        result = self._get_result_bytes()
        self._i2c.readfrom_into(ADDRESS, result)
        voltage = self._get_voltage(result)
        return voltage
