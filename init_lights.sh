#!/usr/bin/env bash

sudo pigpiod -a1
pigs p 17 0
pigs p 22 0
pigs p 24 0

python2 /home/pi/Public/lightshow/lightshow.py >>log.txt 2>&1
