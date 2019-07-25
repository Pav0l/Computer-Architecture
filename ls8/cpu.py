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

    # Add value op_b to register op_a
    def LDI(self, op_a, op_b):
        self.reg[op_a] = op_b
        self.pc += 3

    # print value of register op_a
    def PRN(self, op_a, op_b):
        print(self.reg[op_a])
        self.pc += 2

    # call MUL in ALU unit on op_a and op_b
    def MUL(self, op_a, op_b):
        self.alu("MUL", op_a, op_b)
        self.pc += 3

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

    def CALL(self, register):
        pass
        # store return address (self.pc + 1) in stack

        # then move the pc to the subroutine address

    def RET(self):
        pass
        # pop return value from the stack and store it in self.pc
        # so next cycle will go from there

    # fill out branchtable with available operations
    def initialize_branchtable(self):
        self.branchtable[0b10000010] = self.LDI
        self.branchtable[0b01000111] = self.PRN
        self.branchtable[0b10100010] = self.MUL
        self.branchtable[0b01000110] = self.POP
        self.branchtable[0b01000101] = self.PUSH
        self.branchtable[0b01010000] = self.CALL
        self.branchtable[0b00010001] = self.RET

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
