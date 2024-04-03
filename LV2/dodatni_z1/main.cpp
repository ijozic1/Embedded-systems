#include "mbed.h"

#define T_red 1
#define T_green 0.5
#define T_blue 0.3

DigitalOut red(PTB18);
DigitalOut green(PTB19);
DigitalOut blue(PTB1);

int main() {
    float red_on = T_red;
    float red_off = T_red;

    float green_on = T_green;
    float green_off = T_green;

    float blue_on = T_blue;
    float blue_off = T_blue;

    const float deltaT_red = 0.9/(30*T_red);
    const float deltaT_green = 0.9/(30*T_green);
    const float deltaT_blue = 0.9/(30*T_blue);
    

    while(1) {
        red_on = red_off = T_red;
        green_on = green_off = T_green;
        blue_on = blue_off = T_blue;
        
        while(red_on <= 1.9*T_red) {
            red = 1; 
            wait_us(red_on*(1e6));
            red = 0;
            wait_us(red_off*(1e6));
            
            red_on += deltaT_red;
            red_off -= deltaT_red;
        }

        while(green_on <= 1.9*T_green) {
            green = 1; 
            wait_us(green_on*(1e6));
            green = 0;
            wait_us(green_off*(1e6));
            
            green_on += deltaT_green;
            green_off -= deltaT_green;
        }

        while(blue_on <= 1.9*T_blue) {
            blue = 1; 
            wait_us(blue_on*(1e6));
            blue = 0;
            wait_us(blue_off*(1e6));
            
            blue_on += deltaT_blue;
            blue_off -= deltaT_blue;
        }
        
        while(red_off <= 1.9*T_red) {
            red = 1;
            wait_us(red_on*(1e6));
            red = 0;
            wait_us(red_off*(1e6));
            
            red_on -= deltaT_red;
            red_off += deltaT_red;
        }

        while(green_off <= 1.9*T_green) {
            green = 1;
            wait_us(green_on*(1e6));
            green = 0;
            wait_us(green_off*(1e6));
            
            green_on -= deltaT_green;
            green_off += deltaT_green;
        }

        while(blue_off <= 1.9*T_blue) {
            blue = 1;
            wait_us(blue_on*(1e6));
            blue = 0;
            wait_us(blue_off*(1e6));
            
            blue_on -= deltaT_blue;
            blue_off += deltaT_blue;
        }
    }
}
