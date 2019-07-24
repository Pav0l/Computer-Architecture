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
        self.operations()
        # stack pointer default value
        self.stack_pointer = self.ram[0xF3]

    def LDI(self, op_a, op_b):
        self.reg[op_a] = op_b
        self.pc += 3

    def PRN(self, op_a, op_b):
        print(self.reg[op_a])
        self.pc += 2

    def MUL(self, op_a, op_b):
        self.alu("MUL", op_a, op_b)
        self.pc += 3

    def POP(self, register):
        stack_value = self.ram[self.stack_pointer]
        self.reg[register] = stack_value
        self.stack_pointer -= 1

    def operations(self):
        self.branchtable[0b10000010] = self.LDI
        self.branchtable[0b01000111] = self.PRN
        self.branchtable[0b10100010] = self.MUL
        self.branchtable[0b01000110] = self.POP

    def load(self, file):
        """Load a program into memory."""

        address = 0
        program = []

        with open(file) as f:
            for line in f:
                # remove comments
                line = line.partition('#')[0]
                # remove trailing spaces
                line = line.rstrip()
                if len(line) > 0:
                    # make bin string into integer
                    program.append(int(line, 2))

        for instruction in program:
            self.ram_write(address, instruction)
            address += 1

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
                print(f"Invalid instruction {IR}")
                sys.exit(1)
            else:
                self.branchtable[IR](operand_a, operand_b)
