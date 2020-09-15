"""CPU functionality."""

import sys
"""
## Internal Registers

* `PC`: Program Counter, address of the currently executing instruction
* `IR`: Instruction Register, contains a copy of the currently executing instruction
* `MAR`: Memory Address Register, holds the memory address we're reading or writing
* `MDR`: Memory Data Register, holds the value to write or the value just read
* `FL`: Flags, see below
"""
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0, 0, 0, 0, 0, 0, 0, 0xF4]
        self.pc = 0
        self.running = False

    # takes in register and returns the value at that ram[register]
    def ram_read(self, address):
        return self.ram[address]

    # takes in register and value and sets the ram at that register to the value
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
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
            print(" %02X" % self.registers[i], end='')

        print()

    def HLT(self):  # exit mechanic
        self.running = False

    def LDI(self, register, integer):  # set the value of a register to an integer
        self.registers[register] = integer

    def PRN(self, register):  # print numeric value stored in the given register
        print(self.registers[register])

    def run(self):
        """Run the CPU."""
        self.running = True  # turn on
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        while self.running:
            instruction_register = self.pc
            instruction = self.ram[instruction_register]

            if instruction == LDI:
                self.LDI(operand_a, operand_b)
                self.pc += 2

            elif instruction == PRN:
                self.PRN(operand_a)
                self.pc += 1

            elif instruction == HLT:
                return self.HLT()
            self.pc += 1
