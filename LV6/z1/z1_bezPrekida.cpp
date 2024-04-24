#include "mbed.h"
#include "lpc1114etf.h"

BusOut prikaz1(LED3, LED2, LED1, LED0);
BusOut prikaz2(LED7, LED6, LED5, LED4);
DigitalOut enable(LED_ACT);
DigitalIn taster(Taster_1);

const float T(0.2);
// const float T(2.0);
/*Za T=2.0 se promjena na ledicama desava svako 2s, ali je nedostatak i to sto se stanje
tastera takodjer očitava na svako 2s i nije moguće da do izmjene dođe u kraćem vremenskom
periodu*/
//ako je brze problem sa titranjem
//ako je jos duzi period onda jos izrazeniji problem ocitavanja

int brojac1(0);
int brojac2(0);

int main() {
    enable=0;

    prikaz1=brojac1;
    prikaz2=brojac2;

    while(1) {
        wait_us(T*1e6);
        brojac1=(brojac1+1)%16;
        if (taster) brojac2=(brojac2+1)%16;
        prikaz1=brojac1;
        prikaz2=brojac2;
    }
}