#!/usr/bin/python3

# Ugradbeni sistemi - LV7 - Python3 web server

USE_MQTT=False  # Da li se koristi MQTT
USE_PWM=True    # Da li se koristi PWM

# Ukoliko nisu instalirane Python3 biblioteke http.server, paho.mqtt, urllib.parse i RPi.GPIO, treba ih instalirati
from http.server import BaseHTTPRequestHandler, HTTPServer
import RPi.GPIO as GPIO
import time
#import paho.mqtt.client as mqtt
import urllib.parse

# Ukoliko se koristi drugi MQTT broker, treba podesiti parametre za konekciju
MQTT_BROKER = "18.197.9.31" #"broker.hivemq.com"
MQTT_PORT = 1883
MQTT_USER = ""
MQTT_PASSWORD = ""
# Upisati temu na koju se šalju mjerenja
MQTT_TOPIC_ROOT = "ugradbeni/korisnik1/"

# Upisati IP adresu računara na kome se izvršava web seerver
hostName = "192.168.0.154"
hostPort = 8000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Ugradbeni sistemi - LV7</title></head>", "utf-8"))
            self.wfile.write(bytes("<body><p>Python3 web server</p>", "utf-8"))
            self.wfile.write(bytes("<p>Staza: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
            par = urllib.parse.parse_qs(urllib.parse.urlparse(self.requestline).query)
            print(par)
            
            if USE_PWM:
                OFFSET=10.5
                duty_blue=100-(float(par['ax'][0])+OFFSET)/(2*OFFSET)*100
                duty_green=100-(float(par['ay'][0])+OFFSET)/(2*OFFSET)*100
                duty_red=100-(float(par['az'][0])+OFFSET)/(2*OFFSET)*100
                blue_pwm.ChangeDutyCycle(duty_blue)
                green_pwm.ChangeDutyCycle(duty_green)
                red_pwm.ChangeDutyCycle(duty_red)
                print("duty_blue={}".format(duty_blue))
                print("duty_green={}".format(duty_green))
                print("duty_red={}".format(duty_red))

            if USE_MQTT:            
                mqttclient.publish(MQTT_TOPIC_ROOT+"ax", par['ax'][0])
                mqttclient.publish(MQTT_TOPIC_ROOT+"ay", par['ay'][0])
                mqttclient.publish(MQTT_TOPIC_ROOT+"az", par['az'][0])
                mqttclient.publish(MQTT_TOPIC_ROOT+"lux", par['lux'][0].split()[0])
        except:
            print("{0}: Error in GET request.".format(time.asctime()))
	
def on_connect(client, userdata, flags, rc):
    print("{0}: Connected with result code {1}".format(time.asctime(),str(rc)))

def on_message(client, userdata, msg):
    print("{0}: {1} - {2}".format(time.asctime(),msg.topic,str(msg.payload)))

if USE_MQTT:
    mqttclient = mqtt.Client()
    mqttclient.on_connect = on_connect
    mqttclient.on_message = on_message
    mqttclient.username_pw_set(MQTT_USER,MQTT_PASSWORD)

    mqttclient.connect(MQTT_BROKER, MQTT_PORT, 60)

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

if USE_PWM:
    LED_BLUE=3
    LED_GREEN=5
    LED_RED=7

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_BLUE,GPIO.OUT)
    GPIO.setup(LED_GREEN,GPIO.OUT)
    GPIO.setup(LED_RED,GPIO.OUT)
    blue_pwm = GPIO.PWM(LED_BLUE,500)
    green_pwm = GPIO.PWM(LED_GREEN,500)
    red_pwm = GPIO.PWM(LED_RED,500)
    blue_pwm.start(100)
    green_pwm.start(100)
    red_pwm.start(100)

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))

