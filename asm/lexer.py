import lex as lex
import re

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
        %(t.value[0], t.lineno))
    t.lexer.skip(1)

def lexfile(file):
    " lex the input file "
    lexdata = []

    lexer= lex.lex()
    lexer.input(file)

    tok = lexer.token()
    while tok:
        lexdata.append([tok.type, tok.value, tok.lineno])
        print("\033[37;1m\t%-12s\033[0m%s" %(tok.type, tok.value))
        tok = lexer.token()
    return lexdata # [type, value, lineno]

