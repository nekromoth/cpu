import lex as lex
import re
from color import *

lexererror = False
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
t_LABEL       = r"[a-zA-Z_][a-zA-Z0-9_]*:"
t_CONST       = r"%"
t_DATA        = r"\$"
t_ORIGIN      = r"@"
t_ignore = " [],\t"

def t_SEMICOLON(t):
    r":"
    pass

def t_STRING(t):
    r"\"([^\\\n]|(\\.))*?\""

    # remove QUOTES
    t.value = re.sub(r"^\"|\"$", "", t.value)

    # replace escaped characters (\", \\, \n) with (", \, NEWLINE)
    t.value = re.sub(r"\\\"", "\"", t.value)
    t.value = re.sub(r"\\\\", r"\\", t.value)
    t.value = re.sub(r"\\n", "\n", t.value)
    return t

def t_INTEGER(t):
    r"0b[01_]+|0x[a-fA-F0-9]+|[-+]*[0-9]+"
    if   re.match("0b[01_]+", t.value):         # binary
        t.value = int(re.sub(r"_", "", t.value), 2)     # remove UNDERLINES

    elif re.match("[+-]*[0-9]+", t.value):      # decimal
        t.value = int(t.value, 10)

    elif re.match("0x[a-fA-F0-9]+", t.value):   # hexadecimal
        t.value = int(t.value, 16)

    return t

def t_COMMENT(t):       # handle comments
    r'\#.*'
    pass

def t_newline(t):       # handle newlines
    r"\n"
    t.lexer.lineno += len(t.value)

def t_error(t):         # handle errors
    global lexererror
    lexererror = True

    print("%s\tERROR%s        [%s]  Line %d"
        %(cBR, cR, t.value[0], t.lineno))
    t.lexer.skip(1)

def lexfile(file, lexout):
    global lexererror
    types = []
    values = []
    lines = []

    lexer= lex.lex()
    lexer.input(file)

    tok = lexer.token()
    while tok:
        types.append(tok.type)
        values.append(tok.value)
        lines.append(tok.lineno)

        if lexout:
            print("%s\t%-12s%s [%s]" %(cBW, tok.type, cW, tok.value))
        tok = lexer.token()

    if lexererror:
        print("%sFIX ERRORS" % cBR)
        exit()

    return types, values, lines

