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


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0, 0, 0, 0, 0, 0, 0, 0xF4]
        self.pc = 0
        self.running = False
        self.sp = 7

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

    # takes in register and returns the value at that ram[register]
    def ram_read(self, MAR):
        return self.ram[MAR]

    # takes in register and value and sets the ram at that register to the value
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def HLT(self):  # exit mechanic
        self.running = False

    def LDI(self):  # set the value of a register to an integer
        # register to change is the next line in counter
        new_register = self.ram_read(self.pc+1)
        # value is the line after the designated register
        new_value = self.ram_read(self.pc+2)
        self.registers[new_register] = new_value
        self.pc += 3  # have to skip forward since we used the next 2 lines

    def PRN(self):  # print numeric value stored in the given register
        # read the next line that points to register
        reg = self.ram_read(self.pc+1)
        print(self.registers[reg])  # rint the register requested
        self.pc += 2  # skip the next line

    def run(self):
        """Run the CPU."""
        self.running = True  # turn on
        while self.running:  # while on
            ir = self.ram_read(self.pc)  # run each line
