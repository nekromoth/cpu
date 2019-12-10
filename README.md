# m16 Assembler Reference


### Literals 
A literal can be a string or an integer.

#### String-literals
String-literals start and end with QUOTES(").

	"this is a string literal"

#### Integer-literals

### Comments
Comments are prefixed with a HASH(#) and end with NEWLINE.

	mov r0, r1    # this is a comment
	mov r1, r0    # this is another comment


### Origin-directives
Origin-directives tell the assembler where instructions and data are 
located in file-memory. They are prefixed with an AT(@) followed by a 
SPACE( ) a 16 bit integer-literal and a NEWLINE.
    
    @ [integer-literal]
    @ 0xFFEE 

### Statements
	
Statements contain one instruction and up to three operands.
A statement ends with a comment or a NEWLINE.
Operands can be registers, integer-literals, labels or constants.

	<instruction> 
	<instruction> <operand>
	<instruction> <operand> <operand>
	<instruction> <operand> <operand> <operand>

	hlt
	psh r0
	mov D, S
	str [r0:r1], S

### Labels
	
Labels assign a 16bit (relative) address to an identifer.
The identifier should start with a letter and subsequent characters
can be alphanumeric.

	<identifier>:
		<instuction> <label>

	loop:
		jmp loop
