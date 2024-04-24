from machine import Pin
from time import sleep

sleep(0.1)

leds = [Pin(i, Pin.OUT) for i in range(4, 12)]
encoder_clk = Pin(0, Pin.IN)
encoder_dt = Pin(1, Pin.IN)
encoder_click = Pin(2, Pin.IN)

brojac = 0

def interrupt_routine(pin):
    global brojac
    if encoder_dt.value() == 0:
        brojac -= 1
    else:
        brojac += 1

def click(pin):
    global brojac
    brojac = 0

encoder_clk.irq(handler=interrupt_routine, trigger=Pin.IRQ_FALLING)
encoder_click.irq(handler=click, trigger=Pin.IRQ_RISING)


while True:
    for i in range(8):
        leds[i].value((brojac>>i)&1)
    sleep(0.1)
