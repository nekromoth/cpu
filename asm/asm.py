import re

def perror(msg, token, lineno):
    "print error message"
    print("\t\033[31;1mERROR\033[0;31m %s [%s] on line %d\033[0m"
        % (msg, token, lineno))

def parseint(i):
    if   re.match("0b[01_]", i):       return int(re.sub(r"_", "", i), 2)
    elif re.match("0x[a-fA-F0-9]", i): return int(i, 16)
    elif re.match("[+-]*[0-9]", i):    return int(i, 10)

def assemble(lexdata):
    err = False         # indicates if a error occured during assembly
    ptr = 0x0000        # points to the current address in file-memory
    idd = {}            # identifier dictionary
    #==========================================================================
    #   PHASE 1
    #       assign labels to addresses
    #       allocate data-directives into memory
    #==========================================================================
    for i in range(len(lexdata)):
        ttype = lexdata[i][0]   # token type
        tdata = lexdata[i][1]   # token value/data
        tlnno = lexdata[i][2]   # token line number
        print(ttype, tdata, tlnno)
        if ttype == "ORIGIN":
            if lexdata[i + 1][0] == "INTEGER":
                ptr = parseint(tdata)
                i += 1
            else:
                i += 1
                err = True
                perror("expecting integer", tdata, tlnno)
        elif ttype == "DATA":
            pass
        elif ttype == "CONST":
            pass
        elif ttype == "LABEL":
            pass
        elif ttype == "INSTRUCTION":
            ptr += 2

        else:
            pass
