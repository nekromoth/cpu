# m16 Assembler Reference


### COMMENTS
Comments are prefixed with a HASH(#) and end with NEWLINE.
They are not interpreted by the assembler.

	mov r0, r1    # this is a comment
	mov r1, r0    # this is another comment
---

### STATEMENTS
Statements contain one instruction and up to three operands.
A statement ends with a COMMENT or a NEWLINE.
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

### LITERALS
A literal can be a string or an integer:

**String-literals** start and end with QUOTES(").

	<str-literal>

	"this is a string literal"

Escaped characters within a string are:
	
	\\  =  BACKSLASH(\) 
	\n  =  NEWLINE
	\"  =  QUOTES(")

**Integer-literals** can be Binary, Decimal or Hexadecimal.
	
	<int-literal>

	0b00001111
	0b0000_1111_0000_1111		# for readabillity with UNDERLINE(_)
	65535
	-32000				# decimal numbers can be negative
	0xFF54
	0xabcf
--- 

### ORIGIN DIRECTIVES
Origin-directives tell the assembler where instructions and data are 
located in file-memory. They are prefixed with an AT(@) followed by a 
SPACE( ), 16bit integer-literal and a NEWLINE.
    
    @ <int-literal>

    @ 0xFFEE 
---

### IDENTIFIERS
Identifiers start with a letter. Subsequent characters
can be alphanumeric or a UNDERLINE(_).
	
	identifier			# valid
	Identifier12
	Id3_nt1f13r_

	1dentifier			# invalid
	identifier$!"§		
	i den ti fier
---

### LABLES
Labels assign a 16bit (relative) address to an identifer.

	<identifier>:
		<instuction> <label>

	loop:
		jmp loop
---

### CONSTANTS
Constants prefixed by a PERCENT(%) followed by a SPACE( ) exist 
only in assembler source-code. They act as a absolute-addresses 
or immediate value when assembled (and used).
Exessive bits are cut of to fit the destination.

		% <identifier> <int-literal>

		% VAR20bits 0xF00FF
		set r0, VAR20bits 		# r0 will be 0x00FF   NOT 0xF00FF !!
---

### DATA DIRECTIVES
Data-directives prefixed by a DOLLAR-SIGN($) followed by a SPACE( ), 
allocate data (literals) in file-memory. The end of the data-directive will 
be indicated trough either a COMMENT or a NEWLINE.
Literals are sperated by a COMMA(,).

	$ <literal>, <literal>, ..., <literal>
	
	$ "Hello World", 0
---
