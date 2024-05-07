#!/bin/sh
echo 2 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio2/direction
while true
do
    echo 1 > /sys/class/gpio/gpio2/value
    sleep 1
    echo 0 > /sys/class/gpio/gpio2/value
    sleep 1
done 
