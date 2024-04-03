#include "mbed.h"
#include "lpc1114etf.h"

DigitalOut E(LED_ACT);
BusOut leds(LED0, LED1, LED2, LED3, LED4, LED5, LED6, LED7);

int main() {
    E = 0;
    leds=0;
    
    while(1) {
        for(int i=1; i<16; i*=2){
            leds=i;
            wait_us(1e6);
            leds = 0;
            wait_us(1e6);
        }
    }
}