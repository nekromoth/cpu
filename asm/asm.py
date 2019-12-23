import re
from color import *
from opc import *


def perror(msg, token, ttype, lineno):
    "print error message"
    print("\t%sTYPE ERROR%s %s[%s], %s on line %d%s"
        % (cBR, cR,  ttype, token, msg, lineno, cW))

def r(value):
    if   "r0" == value: value = 0
    elif "r1" == value: value = 1
    elif "r2" == value: value = 2
    elif "r3" == value: value = 3
    elif "r4" == value: value = 4
    elif "r5" == value: value = 5
    elif "r6" == value: value = 6
    elif "r7" == value: value = 7
    elif "XR" == value: value = 8
    elif "FR" == value: value = 9
    elif "SS" == value: value = 10
    elif "SP" == value: value = 11
    elif "IS" == value: value = 12
    elif "IP" == value: value = 13
    elif "RS" == value: value = 14
    elif "RP" == value: value = 15
    return value

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
            adr +=  2
            i += 1

        elif "REGISTER" == types[i]:
            i += 1

        elif "IDENTIFIER" == types[i]:
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

            # 00DS ....  mov D, S
            if "mov" == values[i]:
                i += 1

                if "REGISTER" == types[i]:
                    i += 1
                else:
                    err = True
                    perror("expecting REGISTER", values[i], types[i], lines[i])
                    i += 1

                if "REGISTER" == types[i]:
                    mem.append(MOV<<8 + r(values[i-1])<<4 + r(values[i]))
                    mem.append(0)

                    print("\t@ 0x%04x  %s%s%s  %s, %s"
                        %(adr, cBW, values[i-2], cW, values[i-1], values[i]))
                else:
                    err = True
                    perror("expecting REGISTER", values[i], types[i], lines[i])
                    i += 1

                adr +=  2
                i += 1

            # 01D. IIII  set D, I
            elif "set" == values[i]:
                i += 1

                if "REGISTER" == types[i]:
                    i += 1
                else:
                    err = True
                    perror("expecting REGISTER", values[i], types[i], lines[i])
                    i += 1

                if "INTEGER" == values[i]:
                    mem.append(SET<<8 + values[i-1]<<4)
                    mem.append(values[i] & 0xFFFF)

                    print("\t@ 0x%04x  %s%s%s  %s, %s"
                        %(adr, cBW, values[i-2], cW, values[i-1], values[i]))

                elif "IDENTIFIER" == values[i]:
                    # check if identifier exists
                    #mem.append()
                    print("\t@ 0x%04x  %s%s%s  %s, %s"
                        %(adr, cBW, values[i-2], cW, values[i-1], values[i]))

                else:
                    err = True
                    perror("expecting REGISTER or INTEGER",\
                        values[i], types[i], lines[i])


    # exit the assembler if errors occured
    if err:
        print("%sFIX ERRORS" % cBR)
        exit()
