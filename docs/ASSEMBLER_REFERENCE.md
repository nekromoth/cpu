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

### LABLES
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
can be a sequence or integer or string literals. If needed a label can be placed
in front of the data sequence to hold the first entry.
    <id>: <int|str>, <int|str>, ..., <int|str>

    Data: -34, "Hello World", 0, 0b1111_0000


    <int|str>, <int|str>, ..., <int|str>

    "Hello World", 0
---
