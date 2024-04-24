#include "mbed.h"
#include "lpc1114etf.h"

DigitalOut E(LED_ACT);
BusOut prva_cifra(LED3, LED2, LED1, LED0);
BusOut druga_cifra(LED7, LED6, LED5, LED4);

DigitalOut generisani(dp18);
AnalogIn signal(dp9);

void ispisi(int &brojac){
    if(brojac>99) brojac=0;
    druga_cifra=brojac%10;
    prva_cifra=brojac/10;
}

int main() {
    E=0;
    prva_cifra=0;
    druga_cifra=0;
    
    int brojac=0;

    while (true) {

        generisani=1;
        wait_us(1000);
        generisani=0;
        wait_us(1000);

        if(signal.read()==1){
            brojac++;
            ispisi(brojac);
            while(signal.read()==1) continue;
        }
        //wait_ns(1);
    }
}
//radi OK do 500HZ
//onda jedna ne funkcionira u zavisnosti od toga koja je primarna aktivnost