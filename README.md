# MCP3422
This is a driver for the MCP3424 board.

Modified from https://github.com/benlhy/MCP3422

# Setup
```bash
$ git clone git@github.com:johnbridstrup/mcp3424_driver.git
$ cd mcp3424_driver
$ ./setup.sh
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r dev-requirements.txt
# run the tests
$ pytest
```

# Example script
The example script is for using the MCP3424 behind a TCA9548A multiplexer. After running the setup, hook the board up to the SCL and SDA pins on the GPIO and run 
```bash
$ python test.py
```

from the root project directory. You should see the voltage outputs print to your terminal screen.

# Installing into a project
For now, you can simply copy `mcp3424.py` into your projects `venv/lib/site-packages/` folder to import the driver into your own projects.