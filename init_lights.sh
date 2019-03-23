#!/usr/bin/env bash
sudo killall pigpiod
sudo pigpiod
pigs p 17 0
pigs p 22 0
pigs p 24 0

lightshow_dir=/home/pi/Public/lightshow
#python2 /home/pi/Public/lightshow/lightshow.py
python2 $lightshow_dir/lightshow.py >> $lightshow_dir/log.txt 2>&1
