import lex as lex
import sys
import re

################################################################################
def integer(i):
    if re.match(r"[+-]*[0-9]+", i):
        return int(i, 10)

    elif re.match(r"0b[01_]+"):
        return int(re.sub(r"_", "", i), 2)

    else:
        return int(, 16)
################################################################################
print("")
################################################################################
if len(sys.argv) == 1:
    print("\033[1mASSEMBLER")
    print("\033[1m    usage:  \033[0m ./asm.py  <inputfile>\n")
    #print("\033[1m    options:\033[0m -h    show this page")
    #print("             -s    show additional output")
    exit()
################################################################################
tokens = (
    "INSTRUCTION",
    "IDENTIFIER",
    "REGISTER",
    "INTEGER",
    "STRING",
    "LABEL",
    "CONST",
    "DATA",
    "ORIGIN"
)

t_INSTRUCTION =\
    r"mov|set|str|ld|psh|pop|add|sub|mul|div|cmp|and|or|xor|lsh|rsh"\
    r"hlt|jmp|jc|jnc|jv|jnv|je|jne|js|jns|ja|jna|jb|jnb|jg|jng|jl|jn"
t_IDENTIFIER  = r"[a-zA-Z_][a-zA-Z0-9_]+"
t_REGISTER    = r"r0|r1|r2|r3|r4|r5|r6|r7|XR|FR|SP|SS|IP|IS|RP|RS"
t_STRING      = r"\"([^\\\n]|(\\.))*?\""
t_LABEL       = r"[a-zA-Z_][a-zA-Z0-9_]*:"
t_CONST       = r"%"
t_DATA        = r"\$"
t_ORIGIN      = r"@"
t_ignore = " [],\t"

def t_SEMICOLON(t):     # handle semicolons
    r":"
    pass
def t_INTEGER(t):       # handle integers
    r"0x[a-fA-F0-9]+|[-+]*[0-9]+|0b[01_]+"
    return t
def t_COMMENT(t):       # handle comments
    r'\#.*'
    pass
def t_newline(t):       # handle newlines
    r"\n"
    t.lexer.lineno += len(t.value)
def t_error(t):         # handle errors
    print("\033[31;1m\tERROR \033[0;31m      %s  on line %d" 
        %(t.value[0], tok.lineno))
    t.lexer.skip(1)
################################################################################
try:
    print("\033[1mOpening\033[0;m [%s]" % sys.argv[1])
    with open(sys.argv[1], "r") as file:
        filein = file.read()

except FileNotFoundError:
    print("\033[31;1mError\033[0;31m file not found")
    exit()

print("\n\033[1mLexing")

lexer = lex.lex()
lexer.input(filein)

types = []        # contains types
values = []       # contains corresponding values
lines = []        # contains corresponding line positions

tok = lexer.token()
while tok:
    types.append(tok.type)
    values.append(tok.value)
    lines.append(tok.lineno)

    print("\033[37;1m\t%-12s\033[0m%s" %(tok.type, tok.value))
    tok = lexer.token()
################################################################################

print("\n\033[1mAssembling")

ptr = 0         # points to the current address in file-memory

for i in range(len(types)):
    if types[i] == "ORIGIN":
        if types[i+1] == "INTEGER":
            ptr = integer(values[i+1])
            i += 2
        else:
            print("\033[31;1m\tERROR [%s] expecting an integer. Line %s\033[0m"
                %(types[i+1], lines[i+1]))
                i += 2

    elif types[i] == ""

