#include "mbed.h"
#include "lpc1114etf.h"

DigitalOut leds[]={LED0, LED1, LED2, LED3, LED4, LED5, LED6, LED7};
BusOut leds_off(LED0, LED1, LED2, LED3, LED4, LED5, LED6, LED7);
char keypad[4][4]={
    {'1','2','3','A'},
    {'4','5','6','B'},
    {'7','8','9','C'},
    {'*','0','#','D'}};

DigitalOut rows[4]={dp16, dp15, dp17, dp18};
DigitalIn cols[4]={dp9, dp10, dp11, dp13};

DigitalOut E(LED_ACT);

char readKeypad(){
    for(int i=0; i<4; i++){
        rows[i].write(1);

        for(int j=0; j<4; j++){
            if(cols[j].read()){
                rows[i].write(0);
                return keypad[i][j];
            }
        }

        rows[i].write(0);
    }
    return ' ';
}

int main(){
    E=0;
    //turnLedsOff();
    leds_off=0;
    
    char button=' ';
    bool releassed=true;

    while (true){
        button=readKeypad();
        if(button==' ') releassed=true;

        if(button!=' ' && releassed){
            if(button>='1' && button<='8') leds[int(button)-'0'].write(1);
            else if (button=='C') leds_off=0;//turnLedsOff();

            releassed=false;
        }
    }
}