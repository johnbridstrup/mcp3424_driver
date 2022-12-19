#~/bin/bash

sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_ssh 0

sudo apt update
sudo apt install i2c-tools python3-serial