from machine import Pin, ADC, PWM
import network
import time
import simple

# WiFi configuration
wifi_ssid = "Lab220"
wifi_password = "lab220lozinka"

# MQTT configuration
mqtt_server = "broker.hivemq.com"
mqtt_topic_led1 = b"i&v/led1"
mqtt_topic_led2 = b"i&v/led2"
mqtt_topic_led3 = b"i&v/led3"
mqtt_topic_pot =  b"i&v/potenciometar"
mqtt_topic_taster = b"i&v/taster"
mqtt_client_name = "mbedSim"

# Initialize network
print("Connecting to WiFi: ", wifi_ssid)
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifi_ssid, wifi_password)

# Wait until connected
while not wifi.isconnected():
    pass

print("Connected to WiFi")
print("IP address:", wifi.ifconfig()[0])

# Set up pins
taster = Pin(3, Pin.IN)
led1 = Pin(4, Pin.OUT)
led2 = Pin(5, Pin.OUT)
pot = ADC(Pin(28))
led3 = PWM(Pin(6))
led3.freq(1000)

# MQTT message arrived callback for LED control
def message_arrived_led1(topic, msg):
    print("Message arrived on topic:", topic)
    print("Payload:", msg)
    led1.value(int(float(msg)))

def message_arrived_led2(topic, msg2):
    print("Message arrived on topic:", topic)
    print("Payload:", msg2)
    led2.value(int(float(msg2)))

def message_arrived_led3(topic, msg3):
    print("Message arrived on topic:", topic)
    print("Payload:", msg3)
    led3.duty_u16(int(float(msg3)*65535))

def custom_dispatcher(topic, msg):
    if topic == mqtt_topic_led1:
        message_arrived_led1(topic, msg)
    elif topic == mqtt_topic_led2:
        message_arrived_led2(topic, msg)
    elif topic == mqtt_topic_led3:
        message_arrived_led3(topic, msg)

# Initialize state variables
taster_state = taster.value()
last_pot_value = pot.read_u16()

# Connect to MQTT broker
client = simple.MQTTClient(client_id=mqtt_client_name, server=mqtt_server, port=1883)
client.connect()

# Subscribe to topics
client.set_callback(custom_dispatcher)
client.subscribe(mqtt_topic_led1)
client.set_callback(custom_dispatcher)
client.subscribe(mqtt_topic_led2)
client.set_callback(custom_dispatcher)
client.subscribe(mqtt_topic_led3)


# Main loop
while True:
    # Publish taster state
    
    if taster.value() != taster_state:
        taster_state = taster.value()
        #client.publish(mqtt_topic_taster, str(taster_state))
        buf = "{{\"Taster\": {}}}".format(taster_state)
        client.publish(mqtt_topic_taster, buf)
    
    # Publish potentiometer value
    pot_value = pot.read_u16()
    if pot_value != last_pot_value:
        last_pot_value = pot_value
        #client.publish(mqtt_topic_pot, str(pot_value))
        buf = "{{\"Potenciometar\": {}}}".format(pot_value)
        client.publish(mqtt_topic_pot, buf)
    
    
    # Check for incoming MQTT messages
    client.check_msg()
    

    time.sleep(1)