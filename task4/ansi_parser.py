
def parse(input):
    output = ""
    cursor = 0
    i = 0
    while i < len(input):
        if (input[i] == '\\'):
            if (input[i+1] == 'x'):
                if (input[i+2:i+4] == "01"): cursor = 0
                elif (input[i+2:i+4] == "03"): return ""
                elif (input[i+2:i+4] == "05"): cursor = len(output)
                elif (input[i+2:i+4] == "08"): cursor -= 1; output = output[:-1]
                elif (input[i+2:i+4] == "0d"): cursor += 1#; output += "\n"
                else:
                    if (cursor == len(output)):
                        output += bytes(input[i:i+4], "utf-8").decode('unicode_escape')
                        cursor += 1
                    else:
                        bottom = output[:cursor]
                        top = output[cursor:]
                        output = bottom + bytes(input[i:i+4], "utf-8").decode('unicode_escape') + top
                        cursor += 1
                i += 4
            elif (input[i+1:i+5] == "033["): # I know I know, input validation and all that
                if (input[i+5] == 'A'): cursor += 1; output += "\x1a"; i += 6
                elif (input[i+5] == 'C'): cursor += 1; i += 6
                elif (input[i+5] == 'D'): cursor -= 1; i += 6
                elif (input[i+5] == 'H'): i += 6
                elif (input[i+5:i+7] == '2J'): i += 7
                elif (input[i+5:i+7] == '3~'):
                    temp = output[:cursor]
                    temp += output[cursor+1:]
                    output = temp
                    i += 7
            else:
                if (cursor == len(output)):
                    output += input[i]
                    cursor += 1
                    i += 1
                else:
                    bottom = output[:cursor]
                    top = output[cursor:]
                    output = bottom + input[i] + top
                    cursor += 1
                    i += 1
        elif (cursor == len(output)):
            output += input[i]
            cursor += 1
            i += 1
        else:
            bottom = output[:cursor]
            top = output[cursor:]
            output = bottom + input[i] + top
            cursor += 1
            i += 1
    return output

if __name__ == '__main__':
    test1 = r"I'm having trouble debugging a segmentation fault in my C program. Can you help me figure out how to trace the cause usig `gdb\033[D\033[D\033[D\033[D\033[D\033[Dn\033[C\033[C\033[C\033[C\033[C\033[C`"
    test2 = r"I wwan\033[D\033[D\033[D\033[3~\033[C\033[Ct to teach my daughter financial respoo\x08nsibility. What's a good age to s\x03"
    test3 = r"What are the best practices for writing aaaa\x08\x08\x08nd managing large-scale Python applications"
    test4 = r"-fsSL https://code.visualstudio.com/shell instal\x01curl \x05ler.sh -o vs_code.sh\x0d"
    test5 = r"\033[2J\033[Hgagpt -m 'Can you come up with a very simple Excel formula that is equivalent to XMATCH except it is case sensitive'\x0d"
    print(parse(test1))
    print(parse(test2))
    print(parse(test3))
    print(parse(test4))
    print(parse(test5))
