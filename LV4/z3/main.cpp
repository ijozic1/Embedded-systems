#include "mbed.h"  
#include "lpc1114etf.h"

#define nula   0xff  
#define jedan  0x7f  
#define dva    0x3f  
#define tri    0x1f  
#define cetiri 0x0f  
#define pet    0x07  
#define sest   0x03  
#define sedam  0x01  
#define osam   0x00  

BusOut leds(LED0, LED1, LED2, LED3, LED4, LED5, LED6, LED7);  
AnalogIn potMeter (dp9);  
DigitalOut e(LED_ACT);  

int main() {  
    e = 0;  
    while(true) {
        
    
    if(potMeter < 1./9) leds = nula;  
    else if(potMeter >=1./9 && potMeter < 2*1./9) leds = jedan;  
    else if(potMeter >=2*1./9 && potMeter < 3*1./9) leds = dva;  
    else if(potMeter >=3*1./9 && potMeter < 4*1./9) leds = tri;  
    else if(potMeter >=4*1./9 && potMeter < 5*1./9) leds = cetiri;  
    else if(potMeter >=5*1./9 && potMeter < 6*1./9) leds = pet;  
    else if(potMeter >=6*1./9 && potMeter < 7*1./9) leds = sest;  
    else if(potMeter >=7*1./9 && potMeter < 8*1./9) leds = sedam;  
    else if(potMeter > 8*1./9) leds = osam;
    
    wait_us(10);
 
    }
    
}