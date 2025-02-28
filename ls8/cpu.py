"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.branchtable = {}
        # fill out branchtable
        self.initialize_branchtable()
        # stack pointer default value
        self.stack_pointer = 0xF3
        # internal flags register 0b00000LGE
        # L = less then; G = greater than; E = equal
        self.flags = 0b00000000

    """ START ALU function calls"""

    # call MUL in ALU unit on op_a and op_b
    def MUL(self, op_a, op_b):
        self.alu("MUL", op_a, op_b)
        self.pc += 3

    # call ADD in ALU unit on op_a and op_b
    def ADD(self, op_a, op_b):
        self.alu("ADD", op_a, op_b)
        self.pc += 3

    # call CMP in ALU unit on op_a and op_b
    def CMP(self, op_a, op_b):
        self.alu("CMP", op_a, op_b)
        self.pc += 3

    # call AND in ALU unit on op_a and op_b
    def AND(self, op_a, op_b):
        self.alu("AND", op_a, op_b)
        self.pc += 3

    def OR(self, op_a, op_b):
        self.alu("OR", op_a, op_b)
        self.pc += 3

    # If the value in the second register is 0, the system should print an error message and halt
    def MOD(self, op_a, op_b):
        # run a CMP to compare op_b == 0
        self.CMP(0, op_b)
        # get back to previous RAM pc (idx) before CMP
        self.pc -= 3
        # if E flag == 1  => print an error and HLT, else call ALU
        if self.flags == 0b00000001:
            print("ERROR! Can not MOD by 0")
            sys.exit(1)
        else:
            self.alu("MOD", op_a, op_b)
            self.pc += 3

    def XOR(self, op_a, op_b):
        self.alu("XOR", op_a, op_b)
        self.pc += 3

    def NOT(self, op_a, op_b):
        self.alu("NOT", op_a, op_b)
        self.pc += 2

    def SHL(self, op_a, op_b):
        self.alu("SHL", op_a, op_b)
        self.pc += 3

    def SHR(self, op_a, op_b):
        self.alu("SHR", op_a, op_b)
        self.pc += 3

    """ END ALU function calls"""

    # Add value op_b to register op_a
    def LDI(self, op_a, op_b):
        self.reg[op_a] = op_b
        self.pc += 3

    # print value of register op_a
    def PRN(self, op_a, op_b):
        print(self.reg[op_a])
        self.pc += 2

    # pop a value from the stack to a register
    def POP(self, op_a, op_b):
        stack_value = self.ram[self.stack_pointer]
        self.reg[op_a] = stack_value
        # if you are at the top of the stack with stack pointer
        # do not increase pointer
        if self.stack_pointer != 0xF3:
            self.stack_pointer += 1
        self.pc += 2

    # push a value from a register op_a into the stack
    def PUSH(self, op_a, op_b):
        # decrease the stack pointer
        self.stack_pointer -= 1
        # get value from register op_a
        value = self.reg[op_a]
        # write value to the stack at stack pointer
        self.ram_write(self.stack_pointer, value)
        self.pc += 2

    # Calls a subroutine (function) at the address stored in the register
    def CALL(self, op_a, op_b):
        # store return address (self.pc + 2) in stack (return address is the next instruction address)
        self.stack_pointer -= 1
        return_address = self.pc + 2
        self.ram_write(self.stack_pointer, return_address)

        # then move the pc to the subroutine address
        self.pc = self.reg[op_a]

    # Return from subroutine
    def RET(self, op_a, op_b):
        # pop return value from the stack and store it in self.pc
        stack_value = self.ram[self.stack_pointer]
        # so next cycle will go from there
        self.pc = stack_value

    # Jump to the address stored in the given register op_a
    def JMP(self, op_a, op_b):
        self.pc = self.reg[op_a]

    # If equal flag is set (true), jump to the address stored in the given register
    def JEQ(self, op_a, op_b):
        if self.flags == 0b00000001:
            self.pc = self.reg[op_a]
        else:
            self.pc += 2

    # If E flag is clear (false, 0), jump to the address stored in the given register
    def JNE(self, op_a, op_b):
        if self.flags != 0b00000001:
            self.pc = self.reg[op_a]
        else:
            self.pc += 2

    # fill out branchtable with available operations
    def initialize_branchtable(self):
        self.branchtable[0b10000010] = self.LDI
        self.branchtable[0b01000111] = self.PRN
        self.branchtable[0b10100010] = self.MUL
        self.branchtable[0b10100000] = self.ADD
        self.branchtable[0b10101000] = self.AND
        self.branchtable[0b10101010] = self.OR
        self.branchtable[0b10101011] = self.XOR
        self.branchtable[0b01101001] = self.NOT
        self.branchtable[0b10100100] = self.MOD
        self.branchtable[0b10101100] = self.SHL
        self.branchtable[0b10101101] = self.SHR
        self.branchtable[0b01000110] = self.POP
        self.branchtable[0b01000101] = self.PUSH
        self.branchtable[0b01010000] = self.CALL
        self.branchtable[0b00010001] = self.RET
        self.branchtable[0b10100111] = self.CMP
        self.branchtable[0b01010100] = self.JMP
        self.branchtable[0b01010101] = self.JEQ
        self.branchtable[0b01010110] = self.JNE

    # load asembly instructions from a file
    def load(self, file):
        """Load a program into memory."""

        address = 0

        with open(file) as f:
            for line in f:
                # remove comments
                line = line.partition('#')[0]
                # remove trailing spaces
                line = line.rstrip()
                if len(line) > 0:
                    # make bin string into integer
                    instruction = int(line, 2)
                    self.ram_write(address, instruction)
                    address += 1

    # arithmetic logic unit operations
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] > self.reg[reg_b]:
                self.flags = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flags = 0b00000100
            else:
                self.flags = 0b00000001
        # Bitwise-AND the values in registerA and registerB, then store the result in registerA
        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        # Perform a bitwise-OR between the values in registerA and registerB, storing the result in registerA
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        # Perform a bitwise-XOR between the values in registerA and registerB, storing the result in registerA
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        # Perform a bitwise-NOT on the value in a register
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        # Shift the value in registerA left by the number of bits specified in registerB, filling the low bits with 0
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        # Shift the value in registerA right by the number of bits specified in registerB, filling the high bits with 0
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        # Divide the value in the first register by the value in the second, storing the remainder of the result in registerA
        elif op == "MOD":
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == 0b00000001:
                running = False
            elif IR not in self.branchtable:
                print(f"Invalid instruction {IR} ({bin(IR)})")
                sys.exit(1)
            else:
                self.branchtable[IR](operand_a, operand_b)
