#include "mbed.h"
#include "N5110.h"
#include "lpc1114etf.h"
#include <stdio.h>

AnalogIn potMeter(dp9);
DigitalIn taster(Taster_1);
N5110 lcd(dp4,dp24,dp23,dp25,dp2,dp6,dp18);

char* floatToString(float num) {
    // Allocate memory for the string
    char* str = (char*)malloc(20 * sizeof(char)); // Adjust the size as per your requirement

    // Handle negative numbers
    if (num < 0) {
        *str++ = '-';
        num = -num;
    }

    // Integer part
    int intPart = (int)num;
    int index = 0;
    do {
        str[index++] = intPart % 10 + '0';
        intPart /= 10;
    } while (intPart != 0);

    // Reverse the integer part
    for (int i = 0; i < index / 2; i++) {
        char temp = str[i];
        str[i] = str[index - i - 1];
        str[index - i - 1] = temp;
    }

    // Decimal point
    str[index++] = '.';

    // Fractional part
    float fracPart = num - (int)num;
    for (int i = 0; i < 6; i++) { // Assuming 6 decimal places
        fracPart *= 10;
        int digit = (int)fracPart;
        str[index++] = digit + '0';
        fracPart -= digit;
    }

    // Null-terminate the string
    str[index] = '\0';

    return str;
}

void prikaziOtpor() {
    char otporString[10];
    float otpor = 100000 * potMeter.read();
    sprintf(otporString, "%d", (int)otpor);
    
    lcd.clear();
    lcd.printString("Otpor (Ohm): ", 0, 0);
    lcd.printString(otporString, 0, 2);
}

void prikaziNapon() {
    float refNapon = 3.3;
    float napon = refNapon * potMeter.read();
    char* naponString;

    //sprintf(naponString, "%d", (int)napon);

    naponString = floatToString(napon);

    lcd.clear();
    lcd.printString("Napon (V): ", 0, 0);
    lcd.printString(naponString, 0, 2);
    free(naponString);
}   

int main() {
    //false za prikaz otpora, true za prikaz napona
    lcd.init();
    bool viewMode = false;  
    
    while (true) {
        if(taster == 1) viewMode = !viewMode;

        if(viewMode == false) prikaziOtpor();
        else prikaziNapon();
        wait_us(100);       
    }
}
