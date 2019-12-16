#!/usr/bin/env python3
import sys
import re

from enum import Enum

###############################################################################
#                                REGEX FUCTIONS
###############################################################################
def rm(regex, string):
    "remove"
    return re.sub(regex, "", string)

def rp(regex, replacement, string):
    "replace"
    return re.sub(regex, replacement, string)

def match(regex, string):
    "match"
    return re.match(regex, string)

def split(regex, string):
    "split"
    return re.split(regex, string)

def search(regex, string):
    "search"
    return re.search(regex, string)
###############################################################################
#                                 EXPRESSIONS
###############################################################################
REGISTER = r"r0|r1|r2|r3|r4|r5|r6|r7|XR|FR|SP|SS|IP|IS|RP|RS"
INSTRUCTION = r"mov|set|str|ld|psh|pop|add|sub|mul|div|cmp|and|or|xor|lsh|rsh"\
              r"hlt|jmp|jc|jnc|jv|jnv|je|jne|js|jns|ja|jna|jb|jnb|jg|jng|jl|jn"
BINARY      = r"0b[01_]+"
DECIMAL     = r"[+-]*[0-9]+"
HEXADECIMAL = r"0x[a-fA-F0-9]+"
INT_LITERAL = BINARY + r"|" + DECIMAL + r"|" + HEXADECIMAL
STR_LITERAL = r"\".+\""
IDENTIFIER = r"[a-zA-Z_][a-zA-Z0-9_]"
LABEL = IDENTIFIER + r"|" + r":"
COMMENT = r"#.*$"                 # comment after a statement
DATADIRECTIVE = r"\$"
CONSTANT = r"%"
HEADING_WHITE = r"^\s+"
TRAILING_WHITE = r"s+$"
MULTIPLE_WHITE = r"\s+"
WHITESPACE = r"\s"
NEWLINE = r"\n"
###############################################################################
#                                   LOGGING
###############################################################################
def title(msg):
    "print msg in bold white"
    print("\033[1;37m" + msg + "\033[0;37m")

def error(msg):
    "print msg in bold red"
    print("\033[1;31m" + msg + "\033[0m")
def errln(msg, word, lnn, line):
    " error on line .."
    error("! %s [%s]  Line %d: %s" %(msg, word, lnn, line))
###############################################################################
#                                    LEXER
###############################################################################
def lexer(lines):
    "split the input *.asm (rawlines) file into words (tokens)"
    for i in range(len(lines)):             # go trough every line
        lines[i] = rm(NEWLINE, lines[i])        # remove NEWLINE
        lines[i] = rm(HEADING_WHITE, lines[i])  # remove heading
        lines[i] = rm(TRAILING_WHITE, lines[i]) # and trailing whitespace
        lines[i] = rm(COMMENT, lines[i])        # remove commment

        if search(INSTRUCTION, lines[i]):           # if line == instruction
            lines[i] = rp(r"\[", " ", lines[i])             # remove [
            lines[i] = rp(r"]", " ", lines[i])              # remove ]
            lines[i] = rp(r",", " ", lines[i])              # remove ,
            lines[i] = rp(r":", " ", lines[i])              # remove :

        elif not search(DATADIRECTIVE, lines[i]):   # if line == datadirective
            lines[i] = rp(MULTIPLE_WHITE, " ", lines[i])    # replace multiple
            lines[i] = rm(COMMENT, lines[i])

        else:           # line == datadirective
            lines[i] = datadirlexer(i, lines[i])

    return lines

def datadirlexer(lnn, line):
    i = 0
    words = []
    word = ""
    string = False

    while i < len(line):
        if line[i] == "$":      # ignore data-directive
            words.append("$")
            i += 1

        elif match(WHITESPACE, line[i]):    # ignore whitespace
            i += 1

        elif line[i] == "\"":        # begin/end of string
            word += line[i]
            i += 1

        elif string:               # string literal
            if line[i] == "\\":         # escape sequence
                if line[i + 1] == "\"":     # quotes
                    word += "\""
                    i += 2
                elif line[i + 1] == "n":    # newline
                    word += "\n"
                    i += 2
                elif line[i + 1] == "\\":   # backlash
                    word += "\\"
                    i += 2
                else:                       # invalid
                    errln("! Invalid escape character ",
                        line[i] + line[i + 1], lnn. line)
            else:
                word += line[i]
                i += 1
        else:                        # not string literal
            if line[i] == ",":
                words.append(word)
                word = ""
                i += 1
            elif line[i] == "#":    # start of comment
                break

            else:
                word += line[i]
                i += 1
    words.append(word)
    return words

###############################################################################
def parser():
    "make sence of the individual words the lexer provided"
    pass
###############################################################################
#                               GLOBAL VARIABLES
###############################################################################
gERROR = False          # indicates if the assembly failed
###############################################################################
###############################################################################
###############################################################################
###############################################################################
def main():
    if len(sys.argv) == 1:
        error("! Provide file as argument.")
        exit()

    try:
        title("> Opening: [%s]" %sys.argv[1])
        with open(sys.argv[1], "r") as file:
            rawlines = file.readlines()

    except FileNotFoundError:
        error("! File [%s] not found." %sys.argv[1])
        exit()


    for i, line in enumerate(rawlines):
        print("% 3d: %s" %(i + 1, line), end="")

    lexlines = []
    lexlines = lexer(rawlines)

    for i, line in enumerate(lexlines):
        print(line)


###############################################################################
if __name__ == "__main__": main()
