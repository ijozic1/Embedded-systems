import time
from machine import Pin
time.sleep(0.1) # Wait for USB to become ready

print("Hello, Pi Pico!")

leds = [Pin(i, Pin.OUT) for i in range(4, 12)]

tasteri = [Pin(i, Pin.IN) for i in range(0, 4)]

def prikazi_brojac(broj):
  for i in range(8):
    leds[i].value((broj>>i)&1)
  time.sleep(0.2)

brojac = 0

while True:

  if brojac > 255:
    brojac = 0
  elif brojac < 0:
    brojac = 255

  if tasteri[0].value():
    brojac += 1
    prikazi_brojac(brojac)
    while tasteri[0].value():
      time.sleep(0.1)

  elif tasteri[1].value():
    brojac -= 1
    prikazi_brojac(brojac)
    while tasteri[1].value():
      time.sleep(0.1)

  elif tasteri[2].value():
    brojac = 0
    prikazi_brojac(brojac)
    while tasteri[2].value():
      time.sleep(0.1)

  elif tasteri[3].value():
    brojac = 255
    prikazi_brojac(brojac)
    while tasteri[3].value():
      time.sleep(0.1)