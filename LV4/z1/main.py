import time
from machine import Pin, ADC
time.sleep(0.1) # Wait for USB to become ready

leds = [Pin(i, Pin.OUT) for i in range(4, 12)]
adc = ADC(Pin(28))

def decimal_to_binary_8bits(n):
    # Convert decimal to binary and remove the '0b' prefix
    binary_str = bin(int(n))[2:]
    
    # Prepend zeros until the length is 8
    while len(binary_str) < 8:
        binary_str = '0' + binary_str
    
    # Convert the binary string to a list of integers
    binary_list = [int(bit) for bit in binary_str]
    
    return binary_list

def update_leds(num, leds):
    num_binList = decimal_to_binary_8bits(num)
    for i in range(0, 8):
        leds[i].value(num_binList[i])

def set_t(adc_val):
    return 0.1 + 1.9*adc_val/65535

brojac = 0
t = 0.1
adc_val = adc.read_u16()

while True:
    print(adc.read_u16())

    t = set_t(adc.read_u16())

    brojac += 1
    update_leds(brojac, leds)
    time.sleep(t)

    for i in range(0, 8):
        brojac *= 2
        update_leds(brojac, leds)
        t = set_t(adc.read_u16())
        time.sleep(t)

    brojac = 255
    update_leds(brojac, leds)
    t = set_t(adc.read_u16())
    time.sleep(t)

    pomocna = 256
    for i in range(0, 8):
        brojac -= pomocna/2
        update_leds(brojac, leds)
        t = set_t(adc.read_u16())
        time.sleep(t)
        pomocna /= 2

    brojac = 0