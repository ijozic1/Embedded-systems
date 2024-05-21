// 
// Ugradbeni sistemi
// Primjer korištenja GPIO u asembleru
// Sistem: LPC1114ETF (LPC1114FN28)
//
// Samim Konjicija, 20.12.2023. godine
// 

        .syntax unified
        .cpu cortex-m0  
        .thumb
        .global Vector_Table, start

// inicijalizacija tabele prekidnih vektora
        .text
Vector_Table:
// obavezno je potrebno inicijalizirati stack pointer i postaviti adresu početka programa
    .word     0x10001000    // addr 0x00000000 Top of Stack - inicijalno stanje stack pointer-a
    .word     start         // addr 0x00000004 Reset Handler - adresa početka programa
// ostali prekidi se ne koriste
    .word     0             // addr 0x00000008 NMI
    .word     0             // addr 0x0000000c Hard Fault
    .word     0             // addr 0x00000010 Reserved
    .word     0             // addr 0x00000014 Reserved
    .word     0             // addr 0x00000018 Reserved
    .word     0             // addr 0x0000001c Reserved
    .word     0             // addr 0x00000020 Reserved
    .word     0             // addr 0x00000024 Reserved
    .word     0             // addr 0x00000028 Reserved
    .word     0             // addr 0x0000002c SVC
    .word     0             // addr 0x00000030 Reserved
    .word     0             // addr 0x00000034 Reserved
    .word     0             // addr 0x00000038 PendSV
    .word     0             // addr 0x0000003c SysTick

// početak programa
.thumb_func     

start:
// Konfiguracija GPIO

// Uključivanje clock-a za GPIO i IOCON
        ldr R1,SYSAHBCLKCTRL            // učitavanje adrese registra u R1
        ldr R0,[R1]                     // vrijednost iz registra u R0
        ldr R2,SYSAHBCLKMASK            // učitavanje maske
        orrs R0,R0,R2                   // kombiniranje maske sa očitanom vrijednošću
        str R0,[R1]                     // upis nove vrijednosti u registar

// Aktiviranje GPIO funkcije na pinovima sa LED diodama
// Pin P0.0
        ldr R1,IOCON_PIO0_0
        ldr R0,[R1]
        ldr R2,IOCONMASK_PIO0_0
        orrs R0,R0,R2
        str R0,[R1]
// Pin P0.1
        ldr R1,IOCON_PIO0_1
        ldr R0,[R1]
        ldr R2,IOCONMASK_PIO0_1
        bics R0,R0,R2
        str R0,[R1]
// Pin P0.2
        ldr R1,IOCON_PIO0_2
        ldr R0,[R1]
        ldr R2,IOCONMASK_PIO0_2
        bics R0,R0,R2
        str R0,[R1]
// Pin P0.3
        ldr R1,IOCON_PIO0_3
        ldr R0,[R1]
        ldr R2,IOCONMASK_PIO0_3
        bics R0,R0,R2
        str R0,[R1]
// Pin P0.4
        ldr R1,IOCON_PIO0_4
        ldr R0,[R1]
        ldr R2,IOCONMASK_PIO0_4
        bics R0,R0,R2
        str R0,[R1]
// Pin P0.5
        ldr R1,IOCON_PIO0_5
        ldr R0,[R1]
        ldr R2,IOCONMASK_PIO0_5
        bics R0,R0,R2
        str R0,[R1]
// Pin P0.6
        ldr R1,IOCON_PIO0_6
        ldr R0,[R1]
        ldr R2,IOCONMASK_PIO0_6
        bics R0,R0,R2
        str R0,[R1]
// Pin P0.7
        ldr R1,IOCON_PIO0_7
        ldr R0,[R1]
        ldr R2,IOCONMASK_PIO0_7
        bics R0,R0,R2
        str R0,[R1]
// Konfiguracija GPIO pinova sa LED diodama kao izlaza
        ldr R1,GPIO0DIR
        ldr R0,[R1]
        ldr R2,GPIO0MASK
        orrs R0,R0,R2
        str R0,[R1]

// Aktiviranje GPIO funkcije na pinu PIO1.5 (radi aktiviranja LED dioda)
        ldr R1,IOCON_PIO1_5
        ldr R0,[R1]
        ldr R2,IOCONMASK_PIO1_5
        bics R0,R0,R2
        str R0,[R1]
// Konfiguracija pina P1.5 kao izlaza
        ldr R1,GPIO1DIR
        ldr R0,[R1]
        ldr R2,GPIO1MASK
        orrs R0,R0,R2
        str R0,[R1]
// Postavljanje vrijednosti 0 na pinu P1.5 radi aktiviranja LED dioda
        ldr R1,GPIO1DATA
        ldr R0,[R1]
        ldr R2,NOTGPIO1MASK
        ands R0,R0,R2
        str R0,[R1]
        
// Registar R4 će biti korišten kao brojač, inicijaliziranje na 0
        movs R4, #0

// Glavna petlja 
main_loop:
        ldr R1,GPIO0DATA    // adresa registra GPIO0DATA u registar R1
        movs R0, R4         // stanje brojača u registar R0
        str R0,[R1]         // upis stanja brojača iz R0 u GPIO0DATA

        bl delay            // poziv potprograma za pauzu

        adds R4, #1         // povećanje stanja brojača

        b   main_loop       // skok na početak glavne petlje

// potprogram za pauzu        
delay:  
        ldr R3,DELAYLENGTH  // maksimalna vrijednost brojača u registar R3
                            // određuje trajanje pauze
delay_loop:
        subs R3,R3,#1       // umanjivanje stanja brojača
        bne delay_loop      // ako pauza još traje skok na petlju delay_loop
        bx LR               // povratak iz potprograma

// vrijednosti korištenih konstanti su pohranjene u memorijske lokacije
        .align 2            // poravnanje na parnu adresu
GPIO0DATA:  .word   0x50003ffc          // adresa registra GPIO0DATA
GPIO0DIR:   .word   0x50008000          // adresa registra GPIO0DIR
GPIO0MASK:  .word   0xff                // maska za postavljanje GPIO sa LED diodama kao izlaza
NOTGPIO0MASK:   .word   0xffffff00      // invertovana maska
GPIO1DATA:  .word   0x50013ffc          // adresa registra GPIO1DATA
GPIO1DIR:   .word   0x50018000          // adresa registra GPIO1DIR
GPIO1MASK:  .word   0x20                // maska za postavljanje GPIO P1.5 kao izlaza
NOTGPIO1MASK:   .word   0xffffffdf      // invertovana maska
IOCON_PIO0_0:   .word   0x4004400c      // adresa registra IOCON_PIO0_0
IOCON_PIO0_1:   .word   0x40044010      // adresa registra IOCON_PIO0_1
IOCON_PIO0_2:   .word   0x4004401c      // adresa registra IOCON_PIO0_2
IOCON_PIO0_3:   .word   0x4004402c      // adresa registra IOCON_PIO0_3
IOCON_PIO0_4:   .word   0x40044030      // adresa registra IOCON_PIO0_4
IOCON_PIO0_5:   .word   0x40044034      // adresa registra IOCON_PIO0_5
IOCON_PIO0_6:   .word   0x4004404c      // adresa registra IOCON_PIO0_6
IOCON_PIO0_7:   .word   0x40044050      // adresa registra IOCON_PIO0_7
IOCON_PIO1_5:   .word   0x400440a0      // adresa registra IOCON_PIO1_5
SYSAHBCLKCTRL:  .word   0x40048080      // adresa registra SYSAHBCLKCTRL
SYSAHBCLKMASK:  .word   0x10040         // maska za uključivanje signala sata za GPIO
IOCONMASK_PIO0_0:  .word   0x1          // maska za odabir GPIO funkcije na pinu P0.0
IOCONMASK_PIO0_1:  .word   0x3          // maska za odabir GPIO funkcije na pinu P0.1
IOCONMASK_PIO0_2:  .word   0x3          // maska za odabir GPIO funkcije na pinu P0.2
IOCONMASK_PIO0_3:  .word   0x3          // maska za odabir GPIO funkcije na pinu P0.3
IOCONMASK_PIO0_4:  .word   0x3          // maska za odabir GPIO funkcije na pinu P0.4
IOCONMASK_PIO0_5:  .word   0x3          // maska za odabir GPIO funkcije na pinu P0.5
IOCONMASK_PIO0_6:  .word   0x3          // maska za odabir GPIO funkcije na pinu P0.6
IOCONMASK_PIO0_7:  .word   0x3          // maska za odabir GPIO funkcije na pinu P0.7
IOCONMASK_PIO1_5:  .word   0x3          // maska za odabir GPIO funkcije na pinu P1.5
DELAYLENGTH:    .word   0xfffff         // početno stanje brojača za realizaciju pauze
