import pytest

import busio
from MCP3424.mcp3424 import MCP3424
from unittest.mock import MagicMock

class TestMCP3424:
    I2C = MagicMock()
    def test_invalid_params(self):
        with pytest.raises(ValueError):
            MCP3424(self.I2C, bits=33)
        
        with pytest.raises(ValueError):
            MCP3424(self.I2C, channel=33)

        with pytest.raises(ValueError):
            MCP3424(self.I2C, gain=-44)
