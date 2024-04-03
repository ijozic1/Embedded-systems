from machine import Pin, PWM
import time
time.sleep(0.1) # Wait for USB to become ready

# matrix keyboard
tipke = [['1', '2', '3', 'A'],
         ['4', '5', '6', 'B'],
         ['7', '8', '9', 'C'],
         ['*', '0', '#', 'D']]

# pinovi na koje je povezana
keypad_rows = [21, 22, 26, 27]
keypad_cols = [0, 1, 2, 3]

# prazni nizovi u koje će se dodijeliti Pin(i, Pin.IN/OUT)
col_pins = []
row_pins = []

# dodjela fizickih pinova
for x in range(0,4):
  row_pins.append(Pin(keypad_rows[x], Pin.OUT))
  row_pins[x].value(1)
  col_pins.append(Pin(keypad_cols[x], Pin.IN, Pin.PULL_DOWN))
  col_pins[x].value(0)

# scankeys() - vraca char koji je procitan s tastature 
def scankeys():
  for row in range(4):
    for col in range(4):
      row_pins[row].high()
      key = None

      if col_pins[col].value() == 1:
        print("Tipka: ", tipke[row][col])
        key_press = tipke[row][col]
        return key_press
        time.sleep(0.3)
    
    row_pins[row].low()
  return None

def signal(T, izlaz):
    while(True):
       izlaz.value(0)
       time.sleep(T/2.0)
       izlaz.value(1)
       time.sleep(T/2.0)

    

# 7 - segment display
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
        time.sleep(0.00001)

# izvuci n-tu cifru broja
def daj_cifru(broj, n):
    return broj // 10 ** n % 10

T_current = 0.001
signal_on = False

while True:

  unos = scankeys()
  
  prikazi_broj(int(T_current * 1000))

  if unos == 'A' :
    while unos != 'A':


        
        if unos == '0':
            T_current = 0.001
            time.sleep(1)

        elif unos == '1':
            T_current = 0.002
            time.sleep(1)

        elif unos == '2':
            T_current = 0.003
            time.sleep(1)

        elif unos == '3':
            T_current = 0.004
            time.sleep(1)

        elif unos == '4':
            T_current = 0.005
            time.sleep(1)

        elif unos == '5':
            T_current = 0.006
            time.sleep(1)

        elif unos == '6':
            T_current = 0.007
            time.sleep(1)

        elif unos == '7':
            T_current = 0.008
            time.sleep(1)

        elif unos == '8':
            T_current = 0.009
            time.sleep(1)

        elif unos == '9':
            T_current = 0.01
            time.sleep(1)

        elif unos == 'C':
            T_current += 0.001
            if T_current > 0.01:
                T_current = 0.001
            time.sleep(1)

        elif unos == 'D':
            T_current -= 0.001
            if T_current < 0.001:
                T_current = 0.01
            time.sleep(1)



  prikazi_broj(int(T_current * 1000))
  
  time.sleep(0.0001)
