## ASSEMBLER REFERENCE

### PREFACE
---

### COMMENTS
are prefixed with a HASH and end with NEWLINE.
They are not interpreted by the assembler.

    mov r0, r1    # comment
    mov r1, r0    # another comment
---

### STRING LITERALS
start and end with QUOTES.

    <str>

    "this is a string literal"

Escaped characters within a string are:

    \\  =  BACKSLASH(\)
    \n  =  NEWLINE
    \"  =  QUOTES(")
---

### INTEGER LITERALS
can be Binary, Decimal or Hexadecimal.

    <int>

    0b00001111
    0b0000_1111_0000_1111       # for readabillity with UNDERLINE(_)
    65535
    -32000                      # decimal numbers can be negative
    0xFF54
    0xabcf
---

### ORIGIN DIRECTIVES
tell the assembler where instructions and data are located within file-memory.
They are prefixed with an AT followed by a 16bit integer.

    <@> <int>

    @ 0xFFEE
---

### IDENTIFIERS
start with a letter or UNDERLINE, subsequent characters
can be alphanumeric or an UNDERLINE.

    <id>

    __identifier        # valid
    Identifier12
    Id3_nt1f13r_

    1dentifier          # invalid
    identifier$!"§
    i den ti fier
---

### LABELS
are identifiers suffixed by a COLON. They assign a 16bit (relative) address
to an identifer.

    <id><:>

    loop:
        jmp loop
---

### CONSTANTS
are prefixed by a PERCENT followed by an idetifier and an integer.

        <%> <id> <int>

        % VAR 0xF00FF
        set r0, VAR
---

### DATA
can be a sequence of integer or string literals. If needed a label can be placed
in front of the data sequence to hold the address of the first entry.

    <id>: <int|str>, <int|str>, ..., <int|str>

    Data: -34, "Hello World", 0, 0b1111_0000


    <int|str>, <int|str>, ..., <int|str>

    "Hello World", 0
---
### EXAMPLE
    # calculate the sum of all items in ARRAY

    % ARRAY_LENGTH 8

    @ 0x0000
        set r0, ARRAY           # load the address of ARRAY
        set r1, ARRAY_LENGTH    # load the length of ARRAY
        # r2 will be our sum register of the calculation
        # r3 will be the destination from the load instruction

        loop:           # loop till r1 == 0
            ld r3 (IS:r0)   # load item from array
            add r2, r3      # add item to r2
            add r0, 1       # increment array address
            sub r1, 1       # decrement array legth
            cmp r1, 0   # r1 == 0 ?
            je end      # break if 0
            jmp loop    # continue loop

        end:
            hlt         # halt the processor

    @ 0x0100
        ARRAY: 0, 1, 2, 3, 4, 5, 6, 7

