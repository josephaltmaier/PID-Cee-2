#!/bin/bash

sudo pip3 install --upgrade setuptools
sudo apt-get -y install glib-2.0 libbluetooth-dev pkg-config libboost-thread-dev libbluetooth-dev libglib2.0-dev python-dev libboost-python-dev
sudo pip3 install gattlib
cd ~ || exit
mkdir git
cd git || exit
git clone https://github.com/pybluez/pybluez.git
cd pybluez || exit
sudo python3 setup.py install
sudo pip3 install .[ble]