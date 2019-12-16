#!/usr/bin/env python3

import sys
from lexer import lexfile
from asm import assemble


CW  = "\033[0m"
CBW = "\033[37;1m"
CR  = "\033[0;31m"
CBR = "\033[31;1m"


def main():
    if len(sys.argv) == 1:
        print("%sASSEMBLER" % CBW)
        print("\tusage:    %s./main.py  [inputfile]\n" %(CW))
        exit()
    else:
        try:
            print("%sOpening %s[%s]" %(CBW, CW, sys.argv[1]))
            with open(sys.argv[1], "r") as f:
                file = f.read()
        except FileNotFoundError:
            print("%sERROR %sfile not found.%s" %(CBR, CR, CW))
            exit()
        lexdata = lexfile(file)
        assemble(lexdata)

if __name__ == "__main__": 
    main()
