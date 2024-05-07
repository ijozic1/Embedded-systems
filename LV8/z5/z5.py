try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Unable to import RPi.GPIO library. Run your script using 'sudo'")

from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.output(3, True)
GPIO.output(4, True)

channels = [17, 2]

led = GPIO.PWM(channels[1], 1000)
led.start(100)
currentDuty = 100

while True:
    if GPIO.input(channels[0]):
        currentDuty = currentDuty - 10
        if currentDuty == 0:
            currentDuty = 100
        led.ChangeDutyCycle(currentDuty)
        while GPIO.input(channels[0]):
            pass

    sleep(0.01)
