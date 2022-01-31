#################################################
# ECE 366 Project 3                             #
# Maxwell Thimmig, Charlie Shafer, Jim Palomo   #
#################################################

import os.path as Path

# twoscomp: 2's Complement [return binary (string)]    (string -> string)
# Input: s = binary (string) 
# Return: 2's complement binary (string)
def twoscomp(s):
    for j in reversed(range(len(s))):
        if s[j] == '1':
            break

    t = ""
    for i in range(0, j, 1):        # flip everything
        t += str(1-int(s[i]))

    for i in range(j, len(s), 1):   # until the first 1 from the right
        t += s[i]

    return t                        # return 2's complement binary (string)
    
# twoscomp_dec: 2's Complement [return decimal (int)]     [use for sign extend]
# Input: b = binary (string)
# Return: 2's complement decimal (int)
def twoscomp_dec(b):

    l = len(b)          # length of bit provided

    x = b[:1].zfill(l)  # save the first bit and fill with 0's until original length
    x = x[::-1]         # flip binary

    x = int(x, 2) * -1  # value of binary (unsigned: 10000..0) * -1

    y = int(b[1:], 2)   # value of binary without the first bit

    x += y              # add up differing values

    return x            # return 2's complement decimal (int)

# bin_to_dec: convert binary (string) to decimal (int)  [use for sign extend]
# Input: binary (string)
# Return: Decimal (int)
def bin_to_dec(b):
    if(b[0]=="0"):
        return int(b, base=2)
    else:        
        return twoscomp_dec(b)


# zero_extend: zero extend / unsigned operation (for specific operations)
# Input: binary (string)
# Return: decimal (int)
def zero_extend(b):
    return int(b, base=2)   # given a binary string, get unsigned decimal

# Integer to binary

# itosbin: convert integer (int) to signed binary (string)
# Input: i = integer (int) | n = # of bits of desired binary
# Return: returns signed binary (string)
def itosbin(i, n):
    s = ""
    if i >= 0:
        s = bin(i)[2:].zfill(n)
    else:
        s = bin(0-i)[2:].zfill(n)
        s = twoscomp(s)

    return s

# hex_to_bin: convert hex (string) to binary (string)
# Input: line = hex (string)
# Return: unsigned binary (string)
def hex_to_bin(line):
    h = line.replace("\n", "")
    i = int(h, base=16)
    b = bin(i)
    b = b[2:].zfill(8)
    return b

# neg_int_to_hex:
# Input: x = input integer (int)
# Return: x = 2's complemented hexadecimal (string)
def neg_int_to_hex(x):
    x = bin(x & 0xffffffff)[2:]
    x = hex(int(x,2))[2:].zfill(2)
    x = "0x" + x

    return x

# int_to_hex: convert an decimal (int) to hex (string)
# Input: x = input integer (int)
# Return: hex (string)
def int_to_hex(x):
    if (x < 0):
        x = neg_int_to_hex(x)
    else:
        x = "0x" + str(hex(x))[2:].zfill(8)

    return x

# xor8: perform logic XOR on two 8 bit binary (strings)
# Input: x, y = 8-bit binary (strings)
# Return: XORed binary string
def xor8(x, y):
    s = ""
    for i in range(8):
        if x[i] == y[i]:
            s += '0'
        else:
            s += '1'
    
    return s

# findWidth: special instruction used to find the width of a 8-bit binary code
# Input: s = decimal (string)
# Return: width of the specific decimal translated in 8-bit binary 
def findWidth(s):               # take in decimal string 
    b = int(s)                  # convert string decimal to int decimal
    b = itosbin(b, 8)          # convert integer to binary
    return len(b.strip("0"))    # strip surrounding zeros from 1...1 & return length of remaining bits

# processR: process R-type instructions from machine code (string) to hex (string)
# Input: b = 8 bit binary instruction 
# Return: equivalent instruction in hex (string)
def processR(b):
    b_op = b[0:4]
    b_rx = b[4:6]
    b_ry = b[6:8]
    
    asm = ""

    if (b_op == '0100'):     # SLT (sets $R0 to 0 or 1)
        b_rx = b[4:8]        
        rx = int((b_rx), base=2)

        rx = "$5, $4"

        asm = "slt " + rx      
        
    elif (b_op == '1011'):     # SB
        b_rx = b[4:5]
        b_ry = b[5:8]        
        rx = int((b_rx), base=2)
        ry = int((b_ry), base=2)

        rx = "$" + str(rx)
        ry = "$" + str(ry)

        asm = "sb " + rx + ", " + "0(" + ry + ")" 

    elif (b_op == '0110'):     # SW [store width]
        b_rx = b[4:8]
        rx = int((b_rx), base=2)

        rx = "$" + str(rx)

        asm = "sw " + rx        

    elif (b_op == '0101'):    # inc 
        # b_rx = b[4:8]               # inc R5
        rx  = int((b_rx), base=2)

        rx = "$5"

        asm = "inc "+ rx 

    else:
        print (f'NO idea about op = {b_op}')
    
    return asm  

# processB: process B-type instructions from machine code (string) to hex (string)
# Input: b = 8-bit binary instruction 
# Return: equivalent instruction in hex (string)
def processB(b):
    b_op = b[0:4]
    imm  = b[4:8]

    asm = ""

    if (b_op == '1010'):        # BO ($R0 = 1 --> branch PC += -28; else no branch & PC += 1)
        imm = -6

        imm = str(imm)          # hardwired to -28

        asm = "bo " + imm       # compares R0 {if R0 == 1 --> branch; else no branch}


    else:
        print (f'NO idea about op = {b_op}')

    return asm

# processS: process S-type instructions from machine code (string) to hex (string)
# Input: b = 8-bit binary instruction 
# Return: equivalent instruction in hex (string)
def processS(b):
    b_op = b[0:4]
    b_rx = b[4:6]
    b_ry = b[6:8]

    asm = ""

    if (b_op == '1000'):        # FW [find width]
        rx = int((b_rx), base=2)
        
        rx = "$7"

        asm = "fw " + rx

    elif (b_op == '1001'):      # GA [generate A: (A + B) xor C]
        asm = "ga "             # stores into R1 [R1 = A]

    else:
        print (f'NO idea about op = {b_op}')

    return asm    

# processInit: process B-type instructions from machine code (string) to hex (string)
# Input: b = 8-bit binary instruction 
# Return: equivalent instruction in hex (string)
def processInit(b):
    b_op = b[0:2]
    b_rx = b[2:5]
    imm  = b[5:8]

    asm = ""

    options = [100, 1, -1, 15, 73, 51]
    imm = options[int(imm, 2)]
    
    rx  = int((b_rx), base=2)
    rx = "$" + str(rx)

    imm = str(imm)    

    asm = "init " + rx + ", " + imm

    return asm

# process: determine whether the process provided by machine code (string) is B, R, I type.
# Input: b = 8 bit binary instruction | halt = halt variable used to stop the program
# Return: MIPS equivalent instruction in hex (string) after determining instruction type
def process(b, halt):
    
    if (halt != 1):
        b_op = b[0:4]
        
        if (b_op[:2] == '00'):                                          # Init
            return processInit(b)
        elif (b_op == '1111'):                                          # Halt
            halt = 1
            return "halt"
        elif (b_op == '1010'):                                          # B-type (bo)
            return processB(b)
        elif (b_op == '1000' or b_op == '1001'):                        # S-type (ga/fw)
            return processS(b)
        else:
            return processR(b)                                          # R-type
    else:
        return # nothing since program stopped                          # Program was halted

# disassemble: disassembles 8 bit instructions from input .txt file and appends spliced instruction to a list
# Input: input_file = input .txt file (of 8-bit machine code) | asm_instr = output .txt file (hex equivalent of machine code) | halt = stops program
# Return: list (instr) of all instructions from .txt file
def disassemble(input_file, asm_instr, halt):
    instr = []    # create empty list of user inputs

    ''' reasons for list: 
            1. able to append at the end of list to KEEP ORDER
            2. mutable (change elements in list if necessary)
            3. creating a list data structure using string methods (replace, split)
    '''

    line_count = 0
    if (halt != 1):
        # convert 8 bit machine code from input and write to output file
        for line in input_file:
            line_count += 1
            # bin_str = hex_to_bin(line)
            bin_str = line                              # currently only testing binary
            asmline = process(bin_str, halt) 
            output_file.write(asmline + '\n')

            # splice asmline using string methods and append spliced instruction to list
            asm_instr.append(asmline)                   # save asmline into asm_instr
            asmline = asmline.replace(",", " ")
            asmline = asmline.replace("  ", " ")
            asmline = asmline.replace("$", "")
            asmline = asmline.replace("128(", "")
            asmline = asmline.replace("(", "")
            asmline = asmline.replace(")", "")
            asmline = asmline.split(" ")
            instr.append(asmline)                       # append to another list which results in a list-list data structure
    
    else:
        input_file.close()
        return instr

    output_file.write("\n") # newline in output file to show finished
    input_file.close()      # close input file since we no longer need it
    
    return instr            # return list of listed spliced instructions (list-list)

# outputRegisters: output all 8 registers + pc 
# Input: reg = array holding register data | pc = special registers
# Return: outputted registers via console & output file
def outputRegisters(reg, pc, hexValue):
    pReg = "Register"
    pVal = "Value"
    print(f"{pReg:<15}{pVal:^12}")

    # output header output file
    row_item = [pReg, pVal]
    output = '{:<15}{:^12}'.format(row_item[0], row_item[1])
    output_file.write(output + "\n")

    # output 32 registers from reg array 
    for i in range(len(reg)):
        pReg = "$" + str(i)
        if (hexValue == 0):
            pVal = str(reg[i])
        else:
            pVal = int_to_hex(reg[i])
        print(f"{pReg:<15}{pVal:>12}")
        
        # output to txt file
        row_item = [pReg, pVal]
        output = '{:<15}{:>12}'.format(row_item[0], row_item[1])
        output_file.write(output + "\n")        

    # output special registers
    pReg = "pc"
    if (hexValue == 0):
        pVal = str(pc)
    else:
        pVal = int_to_hex(pc)  

    print(f"{pReg:<15}{pVal:>12}")

    row_item = [pReg, pVal] # output to txt file
    output = '{:<15}{:>12}'.format(row_item[0], row_item[1])
    output_file.write(output + "\n")     

    print("\n")

# outputDataMem: output data memory array in similar format as MARS
# Input: mem = data memory array | hex_start = starting memory address | hex_end = ending memory address 
#        address = user selected hex or decimal address output |  value = user selected hex or decimal value output
# Output: outputted data memory array in console and output file
def outputDataMem(mem, hex_start, hex_end, address, value):
    addr = v1 = v2 = v3 = v4 = v5 = v6 = v7 = v8 = ""

    # headers
    if (address == 0):      # [decimal address]
        addr = "Address"
        v1 = "Value (+0)"
        v2 = "Value (+1)"
        v3 = "Value (+2)"
        v4 = "Value (+3)"
        v5 = "Value (+4)"
        v6 = "Value (+5)"
        v7 = "Value (+6)"
        v8 = "Value (+7)"

        # output header to output .txt file [decimal]
        row_item = [addr, v1, v2, v3, v4, v5, v6, v7, v8]
        output = '|{:>10}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|'.format(row_item[0], row_item[1], row_item[2], row_item[3], row_item[4], row_item[5], row_item[6], row_item[7], row_item[8])
        output_file.write(output + "\n")

    else:                   # [hexadecimal address]
        addr = "Address"
        v1 = "Value (+0)"
        v2 = "Value (+4)"
        v3 = "Value (+8)"
        v4 = "Value (+c)"
        v5 = "Value (+10)"
        v6 = "Value (+14)"
        v7 = "Value (+18)"
        v8 = "Value (+1c)"

        # output header to output .txt file [hex]
        row_item = [addr, v1, v2, v3, v4, v5, v6, v7, v8]
        output = '|{:^10}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|'.format(row_item[0], row_item[1], row_item[2], row_item[3], row_item[4], row_item[5], row_item[6], row_item[7], row_item[8])
        output_file.write(output + "\n")

    print(f"|{addr:>15}|{v1:>15}|{v2:>15}|{v3:>15}|{v4:>15}|{v5:>15}|{v6:>15}|{v7:>15}|{v8:>15}|")

    j = 0

    if (value == 0):        # data memory [decimal values]
        for i in range(hex_start, hex_end, 1):
            if (j % 8 == 0):
                if (address == 1):
                    # addr = "0x" + str(hex(j*4 + 0x0))[2:].zfill(8)
                    addr = "0x" + str(hex(j + 0x0))[2:].zfill(8)
                else:
                    # addr = str(j*4 + 0x0)
                    addr = str(j + 0x0)

                if j < len(mem):
                    v1 = str(mem[j]) 
                else:
                    v1 = 0
    
                if j+1 < len(mem):
                    v2 = str(mem[j+1]) 
                else:
                    v2 = 0
    
                if j+2 < len(mem):
                    v3 = str(mem[j+2]) 
                else:
                    v3 = 0
    
                if j+3 < len(mem):
                    v4 = str(mem[j+3]) 
                else:
                    v4 = 0
    
                if j+4 < len(mem):
                    v5 = str(mem[j+4]) 
                else:
                    v5 = 0
    
                if j+5 < len(mem):
                    v6 = str(mem[j+5]) 
                else:
                    v6 = 0
    
                if j+6 < len(mem):
                    v7 = str(mem[j+6]) 
                else:
                    v7 = 0
    
                if j+7 < len(mem):
                    v8 = str(mem[j+7]) 
                else:
                    v8 = 0
    
                print(f"|{addr:>15}|{v1:>15}|{v2:>15}|{v3:>15}|{v4:>15}|{v5:>15}|{v6:>15}|{v7:>15}|{v8:>15}|")
                row_item = [addr, v1, v2, v3, v4, v5, v6, v7, v8]
                output = '|{:>10}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|'.format(row_item[0], row_item[1], row_item[2], row_item[3], row_item[4], row_item[5], row_item[6], row_item[7], row_item[8])
                output_file.write(output + "\n")    

            j += 1

    else:        # data memory [hexadecimal values]
        for i in range(hex_start, hex_end, 1):
            if (j % 8 == 0):
                if (address == 1):
                    # addr = "0x" + str(hex(j*4 + 0x0))[2:].zfill(8)
                    addr = "0x" + str(hex(j + 0x0))[2:].zfill(8)
                else:
                    # addr = str(j*4 + 0x0)
                    addr = str(j + 0x0)

                if j < len(mem):
                    if (mem[j] < 0):
                        v1 = neg_int_to_hex(mem[j])
                    else:
                        v1 = "0x" + str(hex(mem[j]))[2:].zfill(8)
                else:
                    v1 = "0x" + "".zfill(8)
    
                if j+1 < len(mem):
                    if (mem[j+1] < 0):
                        v2 = neg_int_to_hex(mem[j+1])
                    else:
                        v2 = "0x" + str(hex(mem[j+1]))[2:].zfill(8)
                else:
                    v2 = "0x" + "".zfill(8)
    
                if j+2 < len(mem):
                    if (mem[j+2] < 0):
                        v3 = neg_int_to_hex(mem[j+2])
                    else:
                        v3 = "0x" + str(hex(mem[j+2]))[2:].zfill(8)
                else:
                    v3 = "0x" + "".zfill(8)
    
                if j+3 < len(mem):
                    if (mem[j+3] < 0):
                        v4 = neg_int_to_hex(mem[j+3])
                    else:
                        v4 = "0x" + str(hex(mem[j+3]))[2:].zfill(8)                
                else:
                    v4 = "0x" + "".zfill(8)
    
                if j+4 < len(mem):
                    if (mem[j+4] < 0):
                        v5 = neg_int_to_hex(mem[j+4])
                    else:
                        v5 = "0x" + str(hex(mem[j+4]))[2:].zfill(8)
                else:
                    v5 = "0x" + "".zfill(8)
    
                if j+5 < len(mem):
                    if (mem[j+5] < 0):
                        v6 = neg_int_to_hex(mem[j+5])
                    else:
                        v6 = "0x" + str(hex(mem[j+5]))[2:].zfill(8)
                else:
                    v6 = "0x" + "".zfill(8)
    
                if j+6 < len(mem):
                    if (mem[j+6] < 0):
                        v7 = neg_int_to_hex(mem[j+6])
                    else:
                        v7 = "0x" + str(hex(mem[j+6]))[2:].zfill(8)
                else:
                    v7 = "0x" + "".zfill(8)
                    
    
                if j+7 < len(mem):
                    if (mem[j+7] < 0):
                        v8 = neg_int_to_hex(mem[j+7])
                    else:
                        v8 = "0x" + str(hex(mem[j+7]))[2:].zfill(8)
                else:
                    v8 = "0x" + "".zfill(8)
    
                print(f"|{addr:>15}|{v1:>15}|{v2:>15}|{v3:>15}|{v4:>15}|{v5:>15}|{v6:>15}|{v7:>15}|{v8:>15}|")
                row_item = [addr, v1, v2, v3, v4, v5, v6, v7, v8]
                output = '|{:<10}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|'.format(row_item[0], row_item[1], row_item[2], row_item[3], row_item[4], row_item[5], row_item[6], row_item[7], row_item[8])
                output_file.write(output + "\n")      



            j += 1            
    print("\n")

# outputInstrStats: output instruction statistics (ALU, Jump, branch, memory, other)
# Input: total, alu, jump, branch, memory, other = current values that are held for each count variable
# Return: output instruction statistics on console and output .txt file 
def outputInstrStats(total, alu, jump, branch, memory, other):
    print("Instruction Statistics, Version 1.0")
    output_file.write("\n\nInstruction Statistics, Version 1.0" + "\n")

    print(f"Total:\t{total}\n")
    output_file.write(f"Total:\t{total}\n\n")

    titles = ["ALU:", "Jump:", "Branch:", "Memory:", "Other:"]
    values = [alu, jump, branch, memory, other]
    percentages = [(alu/total)*100, (jump/total)*100, (branch/total)*100, (memory/total)*100, (other/total)*100]
    i = 0
    while i < len(titles):
        print(f"{titles[i]:<8}{values[i]:<8}{percentages[i]:.0f}%")
        output_file.write(f"{titles[i]:<8}{values[i]:<8}{percentages[i]:.0f}%" + "\n")

        i += 1

# Main ---------------------------------------------------------------

print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Project 3 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

input_file = input("Enter input file> ")

file_exists = 0                                         # temp variable to keep track of file exist state 

# check if input file exists 
while (file_exists != 1):
    if Path.isfile(input_file): # file exists
        print("File sucessfully loaded")
        input_file = open(input_file, "r")              # open input file in read mode (r)
        file_exists = 1                                 # file exists so set true
    else: # file does not exist, so ask for valid file
        print("File does not exist")
        file_exists = 0                                 # file does not exists so set false
        input_file = input("Enter input file> ")

output_file = input("Enter desired output file> ")      # ask for user output file name
output_file = open(output_file,"w")                     # create and open output file in write mode (w)
print()
# hardcoded for testing purposes
# input_file = open("input.txt", "r")
# output_file = open("asm.txt", "w")

asm_instr = []

halt = 0

instr = disassemble(input_file, asm_instr, halt)

reg = [0] * 8        # four available register (00 = $0 | 01 = $1 | 10 = $2 | 11 = $3)

mem = [0] * 256      # data memory

line = pc = 0

# instruction statistics
total = alu = jump = branch = memory = other = 0

# output header
pLine = "line"
pInstr = "Instruction"
pResult = "Result"
pPC = "PC"

print(f"{pLine:<15}{pInstr:<35}{pResult:<25}{pPC:<15}")
output_file.write(f"{pLine:<15}{pInstr:<35}{pResult:<25}{pPC:<15}" + "\n")

while (pc < len(instr)):
    cur = instr[pc]                 # give access to instr[] list-list
                                    # first list: separated machine code instructions (access to opcode, rs, rt, rd, sa, func, imm)
                                    # second list: holds the first list within itself and replicates "line numbers"

    line += 1                       # update for next instruction in instr list
    
    if (cur[0] == "bo"):    # branch
            pInstr = asm_instr[pc]
            if (reg[0] == 1):         # $0 == 1?
                pc += -6              # pc = pc + imm
            else:
                pc += 1               # pc = pc + 1

            branch += 1
    
            pResult = "branch to PC " + str(pc)

    # must be fw/ga or sb/sw
    elif (cur[0] == "sb" or cur[0] == "sw" or cur[0] == "fw" or cur[0] == "ga" or cur[0] == "slt"):
        if (cur[0] == "sb"):        # SB
            mem[reg[5]] = reg[1]
            
            pResult = "DM[" + str(reg[int(cur[2])]) + "] = " + str(reg[int(cur[1])])
            memory += 1

        elif (cur[0] == "sw"):       # SW            
            mem[reg[5] + 128] = reg[7]
                        
            pResult = "DM[" + str(reg[5] + 128) + "] = " + str(reg[7])
            memory += 1

        elif (cur[0] == "fw"):       # FW
            reg[7] = findWidth(reg[1])      # R1 = width of 8-bit

            pResult = "Width of A -> $7 = " + str(reg[7])
            alu += 1

        elif (cur[0] == "ga"):      # GA
            w = reg[1]
            x = reg[2]
            y = reg[3]
            z = (reg[1] + reg[2]) ^ reg[3]
            # reg[1] = (reg[1] + reg[2]) ^ reg[3]            
            reg[1] = bin_to_dec(xor8(itosbin((reg[1] + reg[2]), 8), itosbin(reg[3], 8)))           

            pResult = "A = " + str(reg[1])
            alu += 1

        elif (cur[0] == "slt"):     # SLT
            if (reg[5] < reg[4]):  # if x < y 
                reg[0] = 1                             # R0 = 1
            else: # x > y
                reg[0] = 0                             # R0 = 0     

            pResult = str(reg[5]) + " < " + str(reg[4]) + " --> $0" + " = " + str(reg[0]) 
            other += 1

        pInstr = asm_instr[pc]
        pc += 1

    else:   # not fw/ga or sb/sw or branch
        if (cur[0] == "init"):      # INIT 
            
            reg[int(cur[1])] = int(cur[2])

        elif (cur[0] == "inc"):    # INC
            reg[5] = reg[5] + 1

        elif (cur[0] == 'halt'):       # HALT
            print

        else:
            print("Instruction not implemented")
            
        pc += 1

        if (cur[0] == 'halt'):
            other += 1
        else:
            alu += 1

        if (cur[0] != 'halt'):  # HALT
            pResult = "$" + cur[1] + " = " + str(reg[int(cur[1])]) 
        else:
            pInstr = "HALT!!"         
            pResult = "Program Stopped"
            pLine = line
            pPC = pc

            print(f"{pLine:<15}{pInstr:<35}{pResult:<25}{pPC:<15}")
            output_file.write(f"{pLine:<15}{pInstr:<35}{pResult:<25}{pPC:<15}" + "\n")            
            break

        pInstr = asm_instr[pc-1]            

    pLine = line
    pPC = pc

    print(f"{pLine:<15}{pInstr:<35}{pResult:<25}{pPC:<15}")
    output_file.write(f"{pLine:<15}{pInstr:<35}{pResult:<25}{pPC:<15}" + "\n")


print()
output_file.write("\n")

# output registers
outputRegisters(reg, pc, 0)

# output Data Memory
output_file.write("\n")
outputDataMem(mem, 0x0, 0x100, 0, 0)

# output instruction statistics
total = alu + jump + branch + memory + other
outputInstrStats(total, alu, jump, branch, memory, other)
