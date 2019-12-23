#!/usr/bin/env python3

import sys
import re
from lex import lexfile
from asm import assemble
from color import *

def information():
        print("%sASSEMBLER%s" %(cBW, cW))
        print("\t%susage:%s" %(cBW, cW))
        print("\t\t%s%s./main.py  [inputfile] [options]"
            %(cBW, cW))
        print("\t%soptions:%s" %(cBW, cW))
        print("\t\t%s-h  %sdisplay this information"
            %(cBW, cW))
        print("\t\t%s-l  %sdisplay additional lexer output"
            %(cBW, cW))
        #print("\t\t%s-a  %sdisplay additional assembler output"
        #    %(cBW, cW))
        exit()


def main():
    lexout = True
    #asmout = False
    options = ""
    filearg = ""

    # print information if there are no arguments
    if len(sys.argv) == 1:
        print("%sProvide a file.\n" %cBR )
        information()

    # get arguments
    else:
        for arg in sys.argv:
            if re.match(r"-", arg):
                options = arg
            else:
                filearg = arg

    # "parse" options
    if re.search(r"h", options):
        information()
    if re.search(r"l", options):
        lexout = True
    #if re.search(r"a", options):
    #    asmout = True
    if filearg == "":
        information()

    # open 
    try:
        print("%sOpening %s[%s]" %(cBW, cW, sys.argv[1]))
        with open(sys.argv[1], "r") as f:
            print("\t.")
            file = f.read()
    except FileNotFoundError:
        print("%s\tERROR %sfile not found.%s" %(cBR, cR, cW))
        exit()

    # lex
    types = []
    values = []
    lines = []
    print("%sLexing%s" %(cBW, cW))
    types, values, lines = lexfile(file, lexout)

    # assemble
    print("%sAssembling%s" %(cBW, cW))
    assemble(types, values, lines)

    # genate bin
if __name__ == "__main__":
    main()
