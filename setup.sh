#!/usr/bin/env bash

sudo apt update
sudo apt upgrade -y
sudo apt install python python-dev python-pip -y
pip install esptool ampy
