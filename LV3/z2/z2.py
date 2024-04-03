from machine import Pin
import time
time.sleep(0.1) # Wait for USB to become ready

cifre = {
    0: 0b1000000,
    1: 0b1111001,
    2: 0b0100100,
    3: 0b0110000,
    4: 0b0011001,
    5: 0b0010010,
    6: 0b0000010,
    7: 0b1111000,
    8: 0b0000000,
    9: 0b0010000,
    10: 0b1111111
}

mjesto = [Pin(m, Pin.OUT) for m in range(4, 8)]
segmenti = [Pin(s, Pin.OUT) for s in range(8, 15)]
tasteri = [Pin(i, Pin.IN) for i in range(4)]

# prikazi cifru na jednom mjestu
def prikazi_cifru(cifra):
    binarno = cifre[cifra]
    for i in range(7):
        segmenti[i].value(binarno & 1)
        binarno = binarno >> 1

# biranje pozicije ručno
def prikazi_poziciju(pozicija):
    for i in range(4):
        mjesto[i].value(1)
    mjesto[pozicija].value(0)

# prikazivanje kompletnog broja
def prikazi_broj(broj):
    n = 3
    cifra = daj_cifru(broj, n)
    while (n>=0):
        prikazi_cifru(10)
        prikazi_poziciju(3-n)
        prikazi_cifru(cifra)
        n -= 1
        cifra = daj_cifru(broj, n)
        time.sleep(0.0001)

# izvuci n-tu cifru broja
def daj_cifru(broj, n):
    return broj // 10 ** n % 10

# inicijalizacija
auto = False
broj = 0

# main loop
while True:
    # tasteri
    if tasteri[0].value():
        broj += 1
        while (tasteri[0].value()):
          continue
      
    elif tasteri[1].value():
        broj -= 1
        while (tasteri[1].value()):
            continue
        
    elif tasteri[2].value():
        broj = 0
        
    elif tasteri[3].value():
        auto = not auto
        count = 0
        while(tasteri[3].value()):
            continue

    # ukoliko je pritisnut taster za automatsko inkrementiranje
    if auto:
        if count == 720:
            broj += 1
            count = 0
        count += 1
    
    # broj mora ostati u rasponu 0 - 9999
    if broj > 9999:
        broj = 0
    
    if broj < 0:
        broj = 9999

    # prikaži na display-u
    prikazi_broj(broj)
    time.sleep(0.0001)
  



