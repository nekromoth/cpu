# m16 Assembler Reference


### Comments
Comments are prefixed with a HASH(#) and end with NEWLINE.

	mov r0, r1    # this is a comment
	mov r1, r0    # this is another comment
---

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
---

### Literals 
A literal can be a string or an integer.

**String-literals** start and end with QUOTES(").

	<str-literal>

	"this is a string literal"

Escaped characters within a string are:
	
	\\  =  BACKSLASH(\) 
	\n  =  NEWLINE
	\"  =  QUOTES(")

**Integer-literals** types are Binary, Decimal and Hexadecimal
	
	<int-literal>

	0b00001111
	0b0000_1111_0000_1111		# for readabillity with UNDERLINE(_)
	65535
	-32000						# decimal numbers can be negative
	0xFF54
	0xabcf
--- 

### Origin-directives
Origin-directives tell the assembler where instructions and data are 
located in file-memory. They are prefixed with an AT(@) followed by a 
SPACE( ) a 16 bit integer-literal and a NEWLINE.
    
    @ <integer-literal>

    @ 0xFFEE 
---

### Identifiers
Identifiers should start with a letter and subsequent characters
can be alphanumeric or a UNDERLINE(_).
	
	identifier			# valid
	Identifier
	Id3nt1f13r

	1dentifier			# invalid
	identifier$!"§		
	i den ti fier
---

### Labels
Labels assign a 16bit (relative) address to an identifer.

	<identifier>:
		<instuction> <label>

	loop:
		jmp loop
---

### Constants
Constants exist only in the assembler source-code. They act as a 
absolute-addresses or immediate value when assembled.
When the integer-literal is bigger than the intended size the exessive bits
are cut of to fit the destination.

		% <identifier> <integer-literal>

		% VAR20bits 0xF00FF
		set r0, VAR20bits 		# r0 will be 0x00FF / NOT 0xF00FF !!
---

### Data-directives
Data-directives prefixed by a DOLLAR-SIGN($) followed by a SPACE( ), 
allocate data (literals) in file-memory. The end of the data-directive will 
be indicated trough either a COMMENT or a NEWLINE.
Literals are sperated by a COMMA(,).

	$ <literal>, <literal>, ..., <literal>
	
	$ "Hello World", 0
---
