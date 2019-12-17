import re
from color import *

def perror(msg, token, ttype, lineno):
    "print error message"
    print("\t%sTYPE ERROR%s %s(%s), %s on line %d%s"
        % (cBR, cR,  ttype, token, msg, lineno, cW))

def assemble(types, values, lines):
    err = False         # indicates if a error occured during assembly
    adr = 0             # points to the current address in file-memory
    mem = []            # file-memory (holds data)
    idd = {}            # identifier dictionary

    #===========================================================================
    #   PHASE 1
    #       assign values to identifiers
    #       write data into file-memory
    #===========================================================================
    i = 0
    while i < len(types):
        #-----------------------------------------------------------------------
        if "ORIGIN" == types[i]:
            i += 1
            if types[i] == "INTEGER":
                adr = values[i] & 0xFFFF
                print("\t@ 0x%04x" % adr)
                i += 1
            else:
                perror("expecting INTEGER", values[i], types[i], lines[i])
                i += 1
                err = True
        #-----------------------------------------------------------------------
        elif "DATA" == types[i]:
            i += 1
            if types[i] == "IDENTIFIER":
                print("\t@ 0x%04x  %s$%s <%s>" %(adr, cBW, cW, values[i]))
                # check if identifier is already in use
                if values[i] in idd.keys():
                    err = True
                    print("%s\tERROR%s identifier <%s> already defined%s"
                        %(cBR, cR, values[i], cW))
                else:
                    idd[values[i]] = adr
                i += 1
            else:
                print("\t@ 0x%04x  %s$%s " %(adr, cBW, cW))
        #-----------------------------------------------------------------------
        elif "INTEGER" == types[i]:
            mem.append(values[i] & 0xFFFF)
            print("\t    @ 0x%04x  %sint%s %d "
                %(adr, cBW, cW, values[i]))
            adr += 1
            i += 1
        #-----------------------------------------------------------------------
        elif "STRING" == types[i]:
            start = adr
            for c in values[i]:
                mem.append(ord(c) & 0xFF)
                adr += 1
            print("\t    @ 0x%04x - 0x%04x  %sstr%s \"%s\" "
                %(start, adr - 1, cBW, cW, values[i]))
            i += 1
        #-----------------------------------------------------------------------
        elif "CONST" == types[i]:
            i += 1
            if types[i] == "IDENTIFIER":
                i += 1
                if types[i] == "INTEGER":
                    print("\t@ ------  %s%%%s <%s> %d" 
                        %(cBW, cW, values[i-1], values[i]))
                    # check if identifier is already in use
                    if values[i-1] in idd.keys():
                        err = True
                        print("%s\tERROR%s identifier <%s> already defined%s"
                            %(cBR, cR, values[i-1], cW))
                    else:
                        idd[values[i-1]] = values[i]
                    i += 1
                else:
                    perror("expecting INTEGER", values[i], types[i], lines[i])
                    i +=1
                    err = True
            else:
                perror("expecting IDENTIFIER", values[i], types[i], lines[i])
                i += 1
                err = True
        #-----------------------------------------------------------------------
        elif "LABEL" == types[i]:
            print("\t@ 0x%04x  %s:%s <%s> " %(adr, cBW, cW, values[i]))
            # check if identifier is already in use
            if values[i] in idd.keys():
                err = True
                print("%s\tERROR%s identifier <%s> already defined%s"
                    %(cBR, cR, values[i], cW))
            else:
                idd[values[i]] = adr
            i += 1
        #-----------------------------------------------------------------------
        elif "INSTRUCTION" == types[i]:
            print("\t$ [%s] @ 0x%04x" %(values[i], adr))
            adr +=  2
            i += 1

    # exit the assembler if errors occured
    if err:
        print("%sFIX ERRORS" % cBR)
        exit()

    err = False         # indicates if a error occured during assembly
    adr = 0             # points to the current address in file-memory
    i = 0
    #===========================================================================
    #   PHASE 2
    #       encode instructions
    #===========================================================================
    while i < len(types):
        #-----------------------------------------------------------------------
        if "ORIGIN" == types[i]:
            i += 1
        #-----------------------------------------------------------------------
        elif "DATA" == types[i]:
            i += 1
            if types[i] == "IDENTIFIER":
                i += 1
        #-----------------------------------------------------------------------
        elif "INTEGER" == types[i]:
            adr += 1
            i += 1
        #-----------------------------------------------------------------------
        elif "STRING" == types[i]:
            for c in values[i]:
                adr += 1
            i += 1
        #-----------------------------------------------------------------------
        elif "CONST" == types[i]:
            i += 1
            if types[i] == "IDENTIFIER":
                i += 1
                if types[i] == "INTEGER":
                    i += 1
        #-----------------------------------------------------------------------
        elif "LABEL" == types[i]:
            i += 1
        #-----------------------------------------------------------------------
        elif "INSTRUCTION" == types[i]:
            print("\t$ [%s] @ 0x%04x" %(values[i], adr))
            adr +=  2
            i += 1

    # exit the assembler if errors occured
    if err:
        print("%sFIX ERRORS" % cBR)
        exit()
