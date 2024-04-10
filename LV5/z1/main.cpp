#include "mbed.h"
#include "lpc1114etf.h"

AnalogIn pot(AD1); //promijeniti pin za simulator je p15
PwmOut led(LED1);

DigitalOut E(LED_ACT);

int main() {
    E=0;
    led.period_ms(500);
    //led.period_us(50);
    //kod ovog u mikros se intenzitet svjetla mijenja 
    //sa manjim promjenama polozaja potenciometra
    
    while (1) {
        led.write(pot.read()); //podesen duty
        printf("%f \n",pot.read());

        wait_us(10000); //eventualno smanjiti
    }
}