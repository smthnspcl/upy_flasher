#!/usr/bin/env bash

apt update
apt upgrade -y
apt install python python-dev python-pip -y
pip install esptool adafruit-ampy
