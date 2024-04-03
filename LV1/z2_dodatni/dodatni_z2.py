import time
from machine import Pin
time.sleep(0.1) # Wait for USB to become ready

red = Pin(14, Pin.OUT)
green = Pin(12, Pin.OUT)
blue = Pin(13, Pin.OUT)

pins = [red, green, blue]

trajanje = 0.1

while True:
    while trajanje < 1.1:
        for lRGB in [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 0], [1, 1, 1]]:
            for pin, value in zip(pins, lRGB):
                pin.value(value)
            time.sleep(trajanje)
        trajanje += 0.1

    while trajanje > 0.1:
        for lRGB in [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 0], [1, 1, 1]]:
            for pin, value in zip(pins, lRGB):
                pin.value(value)
            time.sleep(trajanje)
        trajanje -= 0.1