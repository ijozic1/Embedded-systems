//
// Ugradbeni sistemi
// Demonstracija korištenja MQTT protokola
//
// Napomena: Svaki student treba koristiti jedinstvenu riječ 
//           umjesto "ugradbeni" u okviru tema
//

#define TEMASUBLED1 "i&v/led1"
#define TEMASUBLED2 "i&v/led2"
#define TEMASUBLED3 "i&v/led3"
#define TEMAPUBPOT  "i&v/potenciometar"
#define TEMAPUBTAST "i&v/taster"


#include "mbed.h"

#define MQTTCLIENT_QOS2 0

#include "MQTTNetwork.h"
#include "MQTTmbed.h"
#include "MQTTClient.h"
#include <string.h>

//==============DIO KODA KOJI TREBA BITI KOMENTARISAN ZA MBED SIMULATOR============
//#define MBED_CONF_APP_WIFI_SSID "ETF-WiFi-Guest"
//#define MBED_CONF_APP_WIFI_PASSWORD "ETF-WiFi-Guest"
//
//#include "ESP8266Interface.h"
//
//ESP8266Interface wifi(PTE0, PTE1);
//==============KRAJ DIJELA KODA KOJI TREBA BITI KOMENTARISAN ZA MBED SIMULATOR============

int arrivedcount = 0;

//==============DIO KODA KOJI TREBA BITI KOMENTARISAN ZA MODUL FRDM-KL25Z============
#define MQTT_CLIENT_NAME "mbedSim"
DigitalIn taster(p5);
DigitalOut led1(p6); //slanje poruka sa -X
DigitalOut led2(p7); //slanje poruke sa MQTT Dash
AnalogIn pot(p15);
PwmOut led3(p21);
//==============KRAJ DIJELA KODA KOJI TREBA BITI KOMENTARISAN ZA MODUL FRDM-KL25Z============

//==============DIO KODA KOJI TREBA BITI KOMENTARISAN ZA MBED SIMULATOR============
//#define MQTT_CLIENT_NAME "FRDM_KL25Z"
//DigitalIn taster(D8);
//DigitalOut led1(LED_RED);
//DigitalOut led2(LED_GREEN);
//AnalogIn pot(A0);
//PwmOut led3(LED_BLUE);
//==============KRAJ DIJELA KODA KOJI TREBA BITI KOMENTARISAN ZA MBED SIMULATOR============

char* str;
double pot_value=-1;
bool taster_state=1;

void messageArrived_led1(MQTT::MessageData& md)
{
    MQTT::Message &message = md.message;
    printf("Message arrived: qos %d, retained %d, dup %d, packetid %d\r\n", message.qos, message.retained, message.dup, message.id);
    printf("Payload %.*s\r\n", message.payloadlen, (char*)message.payload);
    ++arrivedcount;
    str=(char*)message.payload;
    led1=atoi(str);
}

void messageArrived_led2(MQTT::MessageData& md)
{
    MQTT::Message &message = md.message;
    printf("Message arrived: qos %d, retained %d, dup %d, packetid %d\r\n", message.qos, message.retained, message.dup, message.id);
    printf("Payload %.*s\r\n", message.payloadlen, (char*)message.payload);
    ++arrivedcount;
    str=(char*)message.payload;
    led2=atoi(str);
}

void messageArrived_led3(MQTT::MessageData& md)
{
    MQTT::Message &message = md.message;
    printf("Message arrived: qos %d, retained %d, dup %d, packetid %d\r\n", message.qos, message.retained, message.dup, message.id);
    printf("Payload %.*s\r\n", message.payloadlen, (char*)message.payload);
    ++arrivedcount;
    str=(char*)message.payload;
    led3=atof(str);
}


int main(int argc, char* argv[])
{
    printf("Ugradbeni sistemi\r\n");
    printf("Demonstracija korištenja MQTT protokola\r\n\r\n");

    SocketAddress a;

//==============DIO KODA KOJI TREBA BITI KOMENTARISAN ZA MODUL FRDM-KL25Z============
    NetworkInterface *network;
    network = NetworkInterface::get_default_instance();
    
    if (!network) {
        return -1;
    }
    MQTTNetwork mqttNetwork(network);
//==============KRAJ DIJELA KODA KOJI TREBA BITI KOMENTARISAN ZA MODUL FRDM-KL25Z============

//==============DIO KODA KOJI TREBA BITI KOMENTARISAN ZA MBED SIMULATOR============
//    printf("\r\nConnecting to WiFi...\r\n");
//    int ret = wifi.connect(MBED_CONF_APP_WIFI_SSID, MBED_CONF_APP_WIFI_PASSWORD, NSAPI_SECURITY_WPA_WPA2);
//    if (ret != 0) {
//        printf("\r\nConnection error\r\n");
//        return -1;
//    }
//
//    printf("Success\r\n\r\n");
//    printf("MAC: %s\r\n", wifi.get_mac_address());
//    wifi.get_ip_address(&a);
//    printf("IP: %s\r\n", a.get_ip_address());
//    wifi.get_netmask(&a);
//    printf("Netmask: %s\r\n", a.get_ip_address());
//    wifi.get_gateway(&a);
//    printf("Gateway: %s\r\n", a.get_ip_address());
//    printf("RSSI: %d\r\n\r\n", wifi.get_rssi());
//
//    MQTTNetwork mqttNetwork(&wifi);
//==============KRAJ DIJELA KODA KOJI TREBA BITI KOMENTARISAN ZA MBED SIMULATOR============

    MQTT::Client<MQTTNetwork, Countdown> client(mqttNetwork);

    const char* hostname = "broker.hivemq.com";
    int port = 1883;
    printf("Connecting to %s:%d\r\n", hostname, port);
    int rc = mqttNetwork.connect(hostname, port);
    if (rc != 0)
        printf("rc from TCP connect is %d\r\n", rc);
    else
        printf("Connected to broker!\r\n");

    MQTTPacket_connectData data = MQTTPacket_connectData_initializer;
    data.MQTTVersion = 3;
    data.clientID.cstring = MQTT_CLIENT_NAME;
    data.username.cstring = "";
    data.password.cstring = "";
    if ((rc = client.connect(data)) != 0)
        printf("rc from MQTT connect is %d\r\n", rc);

    if ((rc = client.subscribe(TEMASUBLED1, MQTT::QOS0, messageArrived_led1)) != 0)
        printf("rc from MQTT subscribe is %d\r\n", rc);
    else
        printf("Subscribed to %s\r\n", TEMASUBLED1);


    if ((rc = client.subscribe(TEMASUBLED2, MQTT::QOS0, messageArrived_led2)) != 0)
        printf("rc from MQTT subscribe is %d\r\n", rc);
    else
        printf("Subscribed to %s\r\n", TEMASUBLED2);

    if ((rc = client.subscribe(TEMASUBLED3, MQTT::QOS0, messageArrived_led3)) != 0)
        printf("rc from MQTT subscribe is %d\r\n", rc);
    else
        printf("Subscribed to %s\r\n", TEMASUBLED3);

    MQTT::Message message;

    // QoS 0
    char buf[100];
    while(1) {
    
        if (taster_state!=taster) {
            taster_state=taster;
            sprintf(buf, "{\"Taster\": %d}", taster.read());
            message.qos = MQTT::QOS0;
            message.retained = false;
            message.dup = false;
            message.payload = (void*)buf;
            message.payloadlen = strlen(buf);
            rc = client.publish(TEMAPUBTAST, message);
        }
        if (pot_value!=pot) {
            pot_value=pot;
            sprintf(buf, "{\"Potenciometar\": %f}", pot_value);
            message.qos = MQTT::QOS0;
            message.retained = false;
            message.dup = false;
            message.payload = (void*)buf;
            message.payloadlen = strlen(buf);
            rc = client.publish(TEMAPUBPOT, message);
        }

        rc = client.subscribe(TEMASUBLED1, MQTT::QOS0, messageArrived_led1);
        rc = client.subscribe(TEMASUBLED2, MQTT::QOS0, messageArrived_led2);
        rc = client.subscribe(TEMASUBLED3, MQTT::QOS0, messageArrived_led3);

        wait_us(100);
    }

}
