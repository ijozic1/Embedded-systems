#include "mbed.h"
#include "lpc1114etf.h"

DigitalOut E(LED_ACT);
BusOut prva_cifra(LED3, LED2, LED1, LED0);
BusOut druga_cifra(LED7, LED6, LED5, LED4);

DigitalOut generisani(dp18);

InterruptIn signal(dp9);

Ticker t;

int brojac=0;

void ispisi(){
    brojac++;

    if(brojac>99) brojac=0;
    druga_cifra=brojac%10;
    prva_cifra=brojac/10;
}

void generisanje_toggle(){
    generisani = !generisani;
}

int main() {
    E=0;
    generisani=0;

    t.attach_us(&generisanje_toggle, 1000.0);

    signal.rise(&ispisi);

    while (true) {
        wait_ns(1);
    }
}
//bez obzira na visinu frekvencije radi ispravno