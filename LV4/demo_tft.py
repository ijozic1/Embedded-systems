"""
Ugradbeni sistemi 2023
Demo prikaza na TFT displeju ILI9341
rezolucija displeja 320x240
"""

from ili934xnew import ILI9341, color565
from machine import Pin, SPI
from micropython import const
import os
import glcdfont
import tt14
import tt24
import tt32
import time

# Dimenzije displeja
SCR_WIDTH = const(320)
SCR_HEIGHT = const(240)
SCR_ROT = const(2)
CENTER_Y = int(SCR_WIDTH/2)
CENTER_X = int(SCR_HEIGHT/2)

print(os.uname())

# Podešenja SPI komunikacije sa displejem
TFT_CLK_PIN = const(18)
TFT_MOSI_PIN = const(19)
TFT_MISO_PIN = const(16)
TFT_CS_PIN = const(17)
TFT_RST_PIN = const(20)
TFT_DC_PIN = const(15)

# Fontovi na raspolaganju
fonts = [glcdfont,tt14,tt24,tt32]

text = 'RPi Pico/ILI9341'

print(text)
print("Fontovi:")
for f in fonts:
    print(f.__name__)

spi = SPI(
    0,
    baudrate=62500000,
    miso=Pin(TFT_MISO_PIN),
    mosi=Pin(TFT_MOSI_PIN),
    sck=Pin(TFT_CLK_PIN))

print(spi)

display = ILI9341(
    spi,
    cs=Pin(TFT_CS_PIN),
    dc=Pin(TFT_DC_PIN),
    rst=Pin(TFT_RST_PIN),
    w=SCR_WIDTH,
    h=SCR_HEIGHT,
    r=SCR_ROT)

# Brisanje displeja i odabir pozicije (0,0)
display.erase()
display.set_pos(0,0)

# Ispis teksta različitim fontovima, počevši od odabrane pozicije
for ff in fonts:
    display.set_font(ff)
    display.print(text)

# Ispis teksta u drugoj boji
display.set_font(tt24)
display.set_color(color565(255, 255, 0), color565(150, 150, 150))
display.print("\nETF Sarajevo")
display.print("Ugradbeni sistemi")
display.print("Demo micropython-ili9341-RPiPico")

time.sleep(1)

# Pomjeranje sadržaja displeja
for i in range(170):
    display.scroll(1)
    time.sleep(0.01)
    
time.sleep(1)
for i in range(170):
    display.scroll(-1)
    time.sleep(0.01)
    
time.sleep(1)

# Prikaz pravougaonika u odabranoj boji
for h in range(SCR_WIDTH):
    if h > SCR_HEIGHT:
        w = SCR_HEIGHT
    else:
        w = h
        
    display.fill_rectangle(0, 0, w, h, color565(0, 0, 255))
    time.sleep(0.01)

time.sleep(0.5)

#Brisanje displeja
display.erase()

# Dodatna funkcija za crtanje kružnice ispisom pojedinačnih piksela
def draw_circle(xpos0, ypos0, rad, col=color565(255, 255, 255)):
    x = rad - 1
    y = 0
    dx = 1
    dy = 1
    err = dx - (rad << 1)
    while x >= y:
        # Prikaz pojedinačnih piksela
        display.pixel(xpos0 + x, ypos0 + y, col)
        display.pixel(xpos0 + y, ypos0 + x, col)
        display.pixel(xpos0 - y, ypos0 + x, col)
        display.pixel(xpos0 - x, ypos0 + y, col)
        display.pixel(xpos0 - x, ypos0 - y, col)
        display.pixel(xpos0 - y, ypos0 - x, col)
        display.pixel(xpos0 + y, ypos0 - x, col)
        display.pixel(xpos0 + x, ypos0 - y, col)
        if err <= 0:
            y += 1
            err += dy
            dy += 2
        if err > 0:
            x -= 1
            dx += 2
            err += dx - (rad << 1)
    
# Prikaz kružnice korištenjem dodatne funkcije
draw_circle(CENTER_X, CENTER_Y, 100)

# Prikaz kružnica različitim bojama
for c in range(80):
    draw_circle(CENTER_X, CENTER_Y, c, color565(255, 0, 0))
    
for c in range(60):
    draw_circle(CENTER_X, CENTER_Y, c, color565(0, 255, 0))
    
for c in range(40):
    draw_circle(CENTER_X, CENTER_Y, c, color565(0, 0, 255))

time.sleep(2)

display.set_font(tt32)
display.erase()

# Različita orijentacija teksta na displeju
display.set_pos(10,100)
display.rotation=0
display.print('Ugradbeni sistemi 2023')
time.sleep(2)
display.erase()
display.set_pos(10,100)

display.rotation=1
display.init()
display.print('Ugradbeni sistemi 2023')
time.sleep(2)
display.erase()

display.set_pos(10,100)
display.rotation=2
display.init()
display.print('Ugradbeni sistemi 2023')
time.sleep(2)
display.erase()

display.set_pos(10,100)
display.rotation=3
display.init()
display.print('Ugradbeni sistemi 2023')
time.sleep(2)
display.erase()

display.set_pos(10,100)
display.rotation=4
display.init()
display.print('Ugradbeni sistemi 2023')
time.sleep(2)
display.erase()

display.set_pos(10,100)
display.rotation=5
display.init()
display.print('Ugradbeni sistemi 2023')
time.sleep(2)
display.erase()

display.set_pos(10,100)
display.rotation=6
display.init()
display.print('Ugradbeni sistemi 2023')
time.sleep(2)
display.erase()

display.set_pos(10,100)
display.rotation=7
display.init()
display.print('Ugradbeni sistemi 2023')
time.sleep(2)
display.erase()

display.set_pos(10,100)
display.rotation=2
display.init()
display.print('Kraj demo aplikacije')

