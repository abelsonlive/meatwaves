#!/usr/bin/sh
rackup &
cd lib
python meatwaves.py &
cd ..