#include "mbed.h"
#include "lpc1114etf.h"

BusOut prikaz1(LED3, LED2, LED1, LED0);
BusOut prikaz2(LED7, LED6, LED5, LED4);
DigitalOut enable(LED_ACT);
InterruptIn taster(Taster_1);

Ticker t;
Timer debounce;

const float T(0.2);
// const float T(2.0);

int brojac1(0);
int brojac2(0);

void prikaz_brojac1(){
    brojac1=(brojac1+1)%16;
    prikaz1=brojac1;
}

void prikaz_brojac2(){
    if(debounce.read_ms()>=200){
        brojac2=(brojac2+1)%16;
        prikaz2=brojac2;
        debounce.reset();
    }
}

int main() {
    enable=0;
    prikaz1=0;
    prikaz2=0;

    debounce.start();
    t.attach(&prikaz_brojac1, T); //attach prima u sekundama
    taster.rise(&prikaz_brojac2);

    while(1) {
        wait_us(1);
    }
}