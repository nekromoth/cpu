# copy contents form array into new_array 
$ "Hello World", "Hello", 0, 123, 1234, 12345 # xsds
$ "\"Hello World\""

% ARRAY_LENGTH		8
% NEW_ARRAY_SEG		1			# segment of the new array
% NEW_ARRAY_PTR		0xfff0		# pointer of the new array

@ 0x0000
	Main:	
		jmp Copy_array
	hlt

	Copy_array:
		psh	 RS
		psh  RP

		# r1 	Counter 
		# r2	segment of new array
		# r3	pointer of new array
		# r4	pointer of old array
		# r5 	holds the data to copy

		set  r1, 0
		set  r2, NEW_ARRAY_SEG
		set  r3, NEW_ARRAY_PTR
		set	 r4  array
		
		Copy_array_loop:
			ld   r5, [IS:r4]		# load from old array
			str  [r2:r3], r5		# store in new array
			
			add  r1, 1				# increment counter
			cmp  r1, ARRAY_LENGHT	# counter == ARRAY_LENGTH ? loop : end
			
		je   Copy_array_loop_end
		jmp  Copy_array_loop

	Copy_array_loop_end:
		pop  RS
		pop  RP
	ret
			
array:
	$ 100 
	$ 200
	$ 300, 400
	$ 500, 600, 700, 800
