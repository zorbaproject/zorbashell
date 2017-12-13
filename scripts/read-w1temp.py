#!/usr/bin/python3
# -*- coding: utf-8 -*-

from contextlib import contextmanager
import sys, os
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

import pip

required_pkgs = ['w1thermsensor']
installed_pkgs = [pkg.key for pkg in pip.get_installed_distributions()]

for package in required_pkgs:
    if package not in installed_pkgs:
        with suppress_stdout():
            pip.main(['install', package])

try:
    import w1thermsensor
except ImportError:
    print("")


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

try:
    sensor = w1thermsensor.W1ThermSensor()
    temperature_in_celsius = sensor.get_temperature()
    print("Msg:"+str(temperature_in_celsius)+"\\u00B0 C")
except:
    print("")
