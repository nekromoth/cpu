import re

def perror(msg, token, lineno):
    "print error message"
    print("\t\033[31;1mERROR\033[0;31m [%s] %s on line %d\033[0m"
        % (token, msg, lineno))

def parseint(i):
    if   re.match("0b[01_]+", i):       return int(re.sub(r"_", "", i), 2)
    elif re.match("0x[a-fA-F0-9]+", i): return int(i, 16)
    elif re.match("[+-]*[0-9]+", i):    return int(i, 10)

def assemble(tokens, types, lines, asmout):
    err = False         # indicates if a error occured during assembly
    adr = 0             # points to the current address in file-memory
    mem = []            # file-memory (holds data)
    idd = {}            # identifier dictionary
    #===========================================================================
    #   PHASE 1
    #       assign labels to addresses
    #       allocate data-directives into memory
    #===========================================================================
    for i in range(len(tokens)):

        if types[i] == "ORIGIN":
            i += 1
            if types[i] == "INTEGER":
                print("\t@ 0x%04x" % tokens[i])
                adr = tokens[i]
            else:
                perror("expecting INTEGER", tokens[i], lines[i])
                err = True

        elif types[i] == "DATA":
            i += 1
            if types[i] == "IDENTIFIER":
                print("\t$ %s @ 0x%04x" %(tokens[i], adr))
                idd[tokens[i]] = adr
            i += 1
            while True:
                if types[i] == "INTEGER":
                    mem.append(tokens[i])
                    print("\tint [%d]  @ 0x%04x" %(tokens[i], adr))
                    adr += 1
                elif types[i] == "STRING":
                    start = adr
                    string = re.sub(r"^\"|\"$", "", tokens[i])
                    string = re.sub(r"\\\"", "\"", string)
                    string = re.sub(r"\\\\", r"\\", string)
                    #string = re.sub(r"\n", "\n", string)
                    newline = False
                    for c in string:
                        # TODO THIS DOESNT WORK YET !!!
                        # NEWLINE INSERTS AS "\" and "n" not as a single "\n" !!
                        mem.append(ord(c))
                        adr += 1

                    end = adr - 1
                    print("\tstr [%s] @ 0x%04x - 0x%04x" %(string, start, end))
                    print(mem[adr-1])
                else:
                    break
                i += 1

        elif types[i] == "CONST":
            pass
        elif types[i] == "LABEL":
            pass
        elif types[i] == "INSTRUCTION":
            adr +=  2

        else:
            pass
