## ASSEMBLER REFERENCE


### COMMENTS
Comments are prefixed with a HASH and end with NEWLINE.
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

**String-literals** start and end with QUOTES.

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
located in file-memory. They are prefixed with an AT followed by a 
SPACE, 16bit integer-literal and a NEWLINE.
    
    @ <int-literal>

    @ 0xFFEE 
---

### IDENTIFIERS
Identifiers start with a letter. Subsequent characters
can be alphanumeric or a UNDERLINE.
	
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
Constants prefixed by a PERCENT followed by a SPACE, exist 
only in assembler source-code. They act as a absolute-addresses 
or immediate value when assembled - and used.
Exessive bits are cut of to fit the destination.

		% <identifier> <int-literal>

		% VAR20bits 0xF00FF
		set r0, VAR20bits 		# r0 will be 0x00FF   NOT 0xF00FF !!
---

### DATA DIRECTIVES
Data-directives prefixed by a DOLLAR-SIGN followed by a SPACE, 
allocate data (literals) in file-memory. The end of the data-directive will 
be indicated trough either a COMMENT or a NEWLINE.
Literals are sperated by a COMMA(,).

	$ <literal>, <literal>, ..., <literal>
	
	$ "Hello World", 0
---

## COMMENTED ASSEMBLER EXAMPLE
	# COPY CONTENTS FROM ARRAY TO NEW_ARRAY LOCATED AT ANOTHER SEGMENT
	
	% ARRAY_LENGTH		8			# length of source and destination array
	% NEW_ARRAY_SEG		1			# segment of the new array
	% NEW_ARRAY_PTR		0xfff0		# pointer of the new array

	@ 0x0000						# start at address IS:0000

		Main:						# main function
			jmp Copy_array			# jump to copy_array function
		hlt							# halt the cpu when copy_array fuction is done
		

		Copy_array:					# copy array fuction
			
			# OVERVIEW of what registers are in use
			# r1 	Counter 
			# r2	segment of new array
			# r3	pointer of new array
			# r4	pointer of old array
			# r5 	holds the data to copy
			
			psh	 RS					# save return address (to main)
			psh  RP
		
			# set up registers like described in the OVERVIEW
			set  r1, 0
			set  r2, NEW_ARRAY_SEG
			set  r3, NEW_ARRAY_PTR
			set	 r4  array
			

			Copy_array_loop:
				ld   r5, [IS:r4]		# load from old array
				str  [r2:r3], r5		# store in new array
				
				add  r1, 1				# increment counter
				cmp  r1, ARRAY_LENGHT	# counter == ARRAY_LENGTH ? loop : end
				
				je   Copy_array_loop_end	# jump if counter == ARRAY_LENGTH
				jmp  Copy_array_loop		# jump if counter != ARRAY_LENGTH

			Copy_array_loop_end:
				pop  RS			# load return address
				pop  RP		
				ret				# and return
					
	array:			# the array to copy
		$ 100 
		$ 200
		$ 300, 400
		$ 500, 600, 700, 800
