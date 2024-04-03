#include "mbed.h"
#include "lpc1114etf.h"
#include <cmath>

DigitalOut led(LED0);
DigitalOut E(LED_ACT);


int main() {
    E = 0;
    double T = 0.005;
    double on = T;
    bool smjer = true;
        
    while(1) {
        led = 1;
        wait_us(on * 1e6);
        led = 0;
        wait_us((2*T-on)*1e6);
        
        if(smjer && std::abs(on-1.9*T) < 1e-16) smjer = false;
        else if(!smjer && std::abs(on - 0.1*T) < 1e-16) smjer = true;

        if(smjer) on += 3./50*T;
        else on -= 3./50*T;
        
    }
}