# m16 Assembler Reference

### Comments
Comments are prefixed with a HASH(#) and end with NEWLINE.
    mov r0, r1    # this is a comment
    mov r1, r0    # this is another comment

### Origin-directives
Origin-directives tell the assembler where instructions and data are 
located in file-memory. They are prefixed with an **AT(@)** followed by a 
**SPACE( )** a **16-bit integer-literal** and a NEWLINE.
    
    @ [integer-literal]
    @ 0xFFEE 
