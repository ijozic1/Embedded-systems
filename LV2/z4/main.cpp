#include "mbed.h"
#include "lpc1114etf.h"

BusOut leds(LED0, LED1, LED2, LED3, LED4, LED5, LED6, LED7);
DigitalIn taster1(Taster_1);
DigitalIn taster2(Taster_2);

DigitalOut E(LED_ACT);

int main() {
    E = 0;
    leds = 0;

    int trajanje_t1 = 100000;
    int trajanje_t2 = 500000;
    int trajanje=0;

    while(true) {
        while(taster1 == 0 && taster2 == 0) {
            leds = 1;
            wait_us(500000);
            leds = 0;
            wait_us(500000);
            if(taster1==1) trajanje=trajanje_t1;
            else trajanje=trajanje_t2;
        }
        
        for(int i=0; i<=8; ++i) {
            leds = static_cast<int>(pow(2, i));
            wait_us(trajanje);
        }
            
        leds = 255;
        wait_us(trajanje);
        for(int i=8; i>=0; --i) {
            leds = leds - static_cast<int>(pow(2, i));
            wait_us(trajanje);
        }
        
        
    }
}