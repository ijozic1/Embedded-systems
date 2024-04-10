#include "mbed.h"
#define PI 4*atan(1)

AnalogOut signal(PTE30);

//uzlazna rampa
void signal2() {
    for(float i = 0.0; i < 1.0; i += 1./25) {
        signal = i;
        wait_ns(20500);
    }
}

//silazna rampa
void signal3() {
    for(float i = 1.0; i>0; i -= 1./25) {
        signal = i;
        wait_us(39);
    }
}

//triangularni
void signal4() {
    for(float i = 1.0; i>0; i -= 1./12) {
        signal = i;
        wait_us(20);
    }
    for(float i = signal; i < 1; i += 1./12) {
        signal = i;
        wait_us(20);
    }
}

//sinusoida - v&i
void signal1() {
    for(float i = PI/6; i<=PI/2; i += float((PI/2-PI/6)/12)) { //maybe promijeniti sa 12 na 13, NISMO SIGURNI HA HA...haha. Ivona se ne smije.
        signal = sin(i);
        wait_us(20);
    }
    for(float i = PI/2; i<=PI; i += float(PI/50)) {
        signal = sin(i);
        wait_us(20);
    }
    for(float i = PI; i<7*PI/6; i += float(PI/66)) { //maybe kroz 12, ovo je kroz 11, a možda je i 13 hahahah NISMO SIGURNI HAH
        signal = sin(i);
        wait_us(20);
    }
}

// |sin(x)|
void signal5() {
    for(float i = 0; i <= PI; i += float(PI/50)) {
        signal = sin(i);
        wait_ns(1); //podesiti frekvenciju
    }
    /*for(float i = PI/2; i<=PI; i += float(PI/24)) {
        signal = sin(i);
        wait_us(20);
    }*/
}

int main(){
    float i=1;
    const float incr=1./25;
    double fi=0;
    const float inc_sin=2*PI/50;
    while(true) {
        //signal 1
        //signal1();
        /*signal=sin(fi)/2+0.5;
        fi+=inc_sin;
        if(fi>=2*PI) fi=0;
        wait_ns(2); *///treba pogledati sta je sa frekv

        //SIGNAL 2
        //inicijalizirati i na 0 prije petlje
        /*signal = i;
        wait_ns(16000);
        i+=incr;
        if(i>1) i=0;*/

        //SIGNAL 3
        //inicijalizirati i na 1 prije petlje
        /*signal = i;
        wait_ns(15550);
        i-=incr;
        if(i<0) i=1;*/

        //SIGNAL 4
        //signal4();

        //SIGNAL 5
        signal5();
    
    }    
}