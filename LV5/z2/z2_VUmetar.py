from machine import Pin, PWM, ADC
from time import sleep
sleep(0.1) # Wait for USB

# Initialize the photoresistor
photoRes = ADC(Pin(28)) 

# Initialize the LEDs as PWM outputs
leds = [PWM(Pin(i)) for i in range(4, 12)] 

# Set the PWM frequency, 1kHz should do
for led in leds:
    led.freq(10000)

# 1/8 of the max duty cycle
delta = int(65535/8) 

# Set the duty cycle values for LEDs (gradient)
duty = [delta, 2*delta, 3*delta, 4*delta, 5*delta, 6*delta, 7*delta, 65535]
# For good measure
print(duty)

# Turn on as many LEDs as necessary
def update_leds(n_leds):
  for i in range(0, 8):
    if i <= n_leds:  
      leds[i].duty_u16(duty[i])
    else:
      leds[i].duty_u16(0)

# Scale the input voltage. 
#The voltage drop across the photoresistor is never 0V 
# so it needs to be scaled accordingly. Performs a linear transformation.
def scaleVoltage(readVoltage):
  k = 65535/(65535-40000)
  return int(k*readVoltage - 40000*k)
      
    
while True: 
  # Read off the voltage from the photoresistor,
  # scale it and print it for reference
  lum = scaleVoltage(photoRes.read_u16())
  print(lum)

  # Depending on the voltage, turn on as many LEDs as necessary:
  if lum < 0:
    update_leds(-1)
    sleep(0.1)
  elif lum >= 0 and lum < delta:
    update_leds(0)
    sleep(0.1)
  elif lum >= delta and lum < 2*delta:
    update_leds(1)
    sleep(0.1)
  elif lum >= 2*delta and lum < 3*delta:
    update_leds(2)
    sleep(0.1)
  elif lum >= 3*delta and lum < 4*delta:
    update_leds(3)
    sleep(0.1)
  elif lum >= 4*delta and lum < 5*delta:
    update_leds(4)
    sleep(0.1)
  elif lum >= 5*delta and lum < 6*delta:
    update_leds(5)
    sleep(0.1)
  elif lum >= 6*delta and lum <= 7*delta:
    update_leds(6)
    sleep(0.1)
  elif lum >= 7*delta and lum < 8*delta:
    update_leds(7)
    sleep(0.1)
  else :
    update_leds(8)
    sleep(0.1)

  sleep(0.1)