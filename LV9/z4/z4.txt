.data
prompt_num_elements:
    .asciz "Unesite broj elemenata (maksimalno 10):\n"
prompt_elements:
    .asciz "Unesite elemente niza:\n"
prompt_min:
    .asciz "Najmanji broj: %d\n"
prompt_max:
    .asciz "Najveci broj: %d\n"
prompt_range:
    .asciz "Opseg: %d\n"
prompt_median:
    .asciz "Medijan: %d\n"
input_buffer:
    .asciz "                    " @ Buffer for input (20 spaces)
array:
    .space 40                     @ Array to hold up to 10 integers (10 * 4 bytes)
max_elements:
    .word 10
num_elements:
    .word 0

.text
.global _start
.extern printf

_start:
    @ Prompt for the number of elements
    mov     r7, #4                @ syscall number for sys_write
    mov     r0, #1                @ file descriptor 1 (stdout)
    ldr     r1, =prompt_num_elements
    mov     r2, #40               @ length of prompt_num_elements string
    swi     #0

read_num_elements:
    @ Read number of elements
    mov     r7, #3                @ syscall number for sys_read
    mov     r0, #0                @ file descriptor 0 (stdin)
    ldr     r1, =input_buffer     @ address of input buffer
    mov     r2, #20               @ number of bytes to read
    swi     #0

    @ Convert input string to integer (num_elements)
    ldr     r1, =input_buffer     @ address of input buffer
    mov     r2, #0                @ initialize result to 0
    mov     r3, #0                @ initialize sign to positive

    @ Skip leading whitespace
skip_whitespace_num:
    ldrb    r4, [r1], #1          @ load byte and increment r1
    cmp     r4, #' '              @ check if byte is a space
    beq     skip_whitespace_num   @ skip if it is a space
    cmp     r4, #'-'              @ check if byte is '-'
    bne     check_digit_num       @ if not '-', check if digit
    mov     r3, #1                @ set sign to negative
    b       skip_whitespace_num   @ continue skipping

check_digit_num:
    sub     r4, r4, #'0'          @ convert ASCII to digit
    cmp     r4, #9                @ check if valid digit (0-9)
    bhi     end_conversion_num    @ if not valid, end conversion

    mov	    r5, r2, lsl #3	      @r5 = r2 * 8
    add	    r2, r5, r2, lsl #1	  @r2 = r5 + r2 * 2 = r2 * 10

    add     r2, r2, r4            @ add the digit to result
    b       skip_whitespace_num   @ continue conversion

end_conversion_num:
    cmp     r3, #0                @ check if number is negative
    beq     store_num_elements    @ if not, skip negation
    rsb     r2, r2, #0            @ negate the result

store_num_elements:
    ldr     r0, =max_elements     @ load maximum number of elements
    ldr     r1, [r0]              @ load max value into r1
    cmp     r2, r1                @ compare num_elements with max_elements
    bhi     exit_program_error    @ if num_elements > max_elements, read again
    ldr     r0, =num_elements     @ load address of num_elements
    str     r2, [r0]              @ store number of elements

    @ Prompt for the elements
    mov     r7, #4                @ syscall number for sys_write
    mov     r0, #1                @ file descriptor 1 (stdout)
    ldr     r1, =prompt_elements
    mov     r2, #23               @ length of prompt_elements string
    swi     #0

read_elements:
    ldr     r0, =num_elements     @ load address of num_elements
    ldr     r3, [r0]              @ load num_elements into r3
    mov     r4, #0                @ initialize index to 0
read_element_loop:
    cmp     r4, r3                @ compare index with num_elements
    bge     selection_sort        @ if index >= num_elements, exit loop

    @ Read each element
    mov     r7, #3                @ syscall number for sys_read
    mov     r0, #0                @ file descriptor 0 (stdin)
    ldr     r1, =input_buffer     @ address of input buffer
    mov     r2, #20               @ number of bytes to read
    swi     #0

    @ Convert input string to integer
    ldr     r1, =input_buffer     @ address of input buffer
    mov     r2, #0                @ initialize result to 0
    mov     r5, #0                @ initialize sign to positive

    @ Skip leading whitespace
skip_whitespace:
    ldrb    r6, [r1], #1          @ load byte and increment r1
    cmp     r6, #' '              @ check if byte is a space
    beq     skip_whitespace       @ skip if it is a space
    cmp     r6, #'-'              @ check if byte is '-'
    bne     check_digit           @ if not '-', check if digit
    mov     r5, #1                @ set sign to negative
    b       skip_whitespace       @ continue skipping

check_digit:
    sub     r6, r6, #'0'          @ convert ASCII to digit
    cmp     r6, #9                @ check if valid digit (0-9)
    bhi     end_conversion        @ if not valid, end conversion

    mov	    r7, r2, lsl #3	      @r7 = r2 * 8
    add	    r2, r7, r2, lsl #1	  @r2 = r7 + r2 * 2 = r2 * 10

    add     r2, r2, r6            @ add the digit to result
    b       skip_whitespace       @ continue conversion

end_conversion:
    cmp     r5, #0                @ check if number is negative
    beq     store_element         @ if not, skip negation
    rsb     r2, r2, #0            @ negate the result

store_element:
    ldr     r0, =array            @ load address of array
    add     r0, r0, r4, lsl #2    @ calculate address of array[r4]
    str     r2, [r0]              @ store the element
    add     r4, r4, #1            @ increment index
    b       read_element_loop     @ repeat for the next element

selection_sort:
    mov     r4, #0                @ i = 0
    ldr     r0, =num_elements     @ load address of num_elements
    ldr     r3, [r0]              @ load num_elements into r3

outer_loop:
    cmp     r4, r3                @ if (i >= 20)
    bge     print_results         @ break

    mov     r6, r4                @ min_index = i
    add     r5, r4, #1            @ j = i + 1

inner_loop:
    cmp     r5, r3                @ if (j >= 20)
    bge     update_min            @ break
    ldr     r1, =array            @ load address of array
    ldr     r8, [r1, r5, LSL #2]  @ r8 = tekst[j]
    ldr     r7, [r1, r6, LSL #2]  @ r7 = tekst[min_index]
    cmp     r8, r7                @ if (tekst[j] < tekst[min_index])
    bge     skip_update           @ skip if r8 >= r7
    mov     r6, r5                @ min_index = j

skip_update:
    add     r5, r5, #1            @ j = j + 1
    b inner_loop                  @ continue inner loop

update_min:
    cmp     r4, r6                @ if (i != min_index)
    beq     no_swap               @ skip swap if i == min_index

    ldr     r1, =array
    ldr     r8, [r1, r4, LSL #2]  @ r8 = tekst[i]
    ldr     r7, [r1, r6, LSL #2]  @ r7 = tekst[min_index]
    str     r7, [r1, r4, LSL #2]  @ tekst[i] = tekst[min_index]
    str     r8, [r1, r6, LSL #2]  @ tekst[min_index] = tekst[i]

no_swap:
    add     r4, r4, #1            @ i = i + 1
    b outer_loop                  @ continue outer loop

print_results:
    @ Calculate min, max, range, and median
    ldr     r3, =num_elements
    ldr     r3, [r3]
    ldr     r0, =array            @ load address of array
    ldr     r1, [r0]              @ load min element (first element)
    add     r2, r0, r3, lsl #2    @ address of array[num_elements-1]
    sub     r2, r2, #4            @ address of the last element
    ldr     r2, [r2]              @ load max element (last element)
    sub     r3, r2, r1            @ calculate range (max - min)

    @ Calculate median
    ldr     r4, =num_elements     @ load address of num_elements
    ldr     r5, [r4]              @ load num_elements into r5
    mov     r6, r5, lsr #1        @ calculate index for median (r5 / 2)
    tst     r5, #1                @ check if num_elements is odd
    beq     even_median

    @ Odd number of elements
    ldr     r0, =array            @ load address of array
    add     r7, r0, r6, lsl #2    @ address of array[r6]
    ldr     r7, [r7]              @ load median element
    b       median_calculated

    even_median:
    @ Even number of elements: take the average of the two middle elements
    ldr     r0, =array            @ load address of array
    add     r7, r0, r6, lsl #2    @ address of array[r6]
    ldr     r7, [r7]              @ load element at array[r6]
    sub     r6, r6, #1            @ index for the previous middle element
    add     r0, r0, r6, lsl #2    @ address of array[r6-1]
    ldr     r6, [r0]              @ load element at array[r6-1]
    add     r7, r7, r6            @ sum the two middle elements
    mov     r7, r7, lsr #1        @ divide by 2 to get the average

median_calculated:
    nop
exit_program:
    @ Write the result and exit the program

    @ Copy the results into safe registers
    mov r10, r1
    mov r9, r2
    mov r8, r3
    mov r6, r7

    @ Print results using printf:

    @ Print min
    push {fp, lr}
    add     fp, sp, #4
    ldr     r0, =prompt_min
    mov     r1, r10
    bl      printf                @ call printf with r0 text and r1 %d
    nop
    sub     sp, fp, #4
    pop     {fp, lr}

    @ Print max
    push {fp, lr}
    add     fp, sp, #4
    ldr     r0, =prompt_max
    mov     r1, r9
    bl      printf                @ call printf with r0 text and r1 %d
    nop
    sub     sp, fp, #4
    pop     {fp, lr}

    @ Print range
    push {fp, lr}
    add     fp, sp, #4
    ldr     r0, =prompt_range
    mov     r1, r8
    bl      printf                @ call printf with r0 text and r1 %d
    nop
    sub     sp, fp, #4
    pop     {fp, lr}

    @ Print median
    push {fp, lr}
    add     fp, sp, #4
    ldr     r0, =prompt_median
    mov     r1, r6
    bl      printf                @ call printf with r0 text and r1 %d
    nop
    sub     sp, fp, #4
    pop     {fp, lr}

    @ Exit the program
    mov     r7, #1                @ syscall number for sys_exit
    mov     r0, #0                @ exit code
    swi     #0                    @ make the syscall

exit_program_error:
       @ mov     r7, #1                @ syscall number for sys_exit
       @ mov     r0, #12               @ exit code
       @ swi     #0                    @ make the syscall
       b         _start                @ ask for user input again


