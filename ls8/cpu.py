"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0, 0, 0, 0, 0, 0, 0, 0xF4]
        self.pc = 0
        self.running = False
        self.sp = 7
        self.branch_table = {  # holds all commands
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b00000001: self.HLT,
            0b01000101: self.PUSH,
            0b01000110: self.POP
        }

    def load(self):
        """Load a program into memory."""

        address = 0
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r') as f:
                for current_line in f:
                    if current_line == "\n" or current_line[0] == "#":
                        continue
                    else:
                        self.ram[address] = int(current_line.split()[0], 2)

                    address += 1
        else:
            raise Exception('Enter a filename')

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
            self.pc += 3
        elif op == "MUL":  # multiply 2 values and save in the first register
            self.registers[self.ram[reg_a]] *= self.registers[self.ram[reg_b]]
            self.pc += 3
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

    def ADD(self):
        self.alu("ADD", self.ram[self.pc+1], self.ram[self.pc+2])

    def HLT(self):
        self.running = False

    def LDI(self):  # Set the value of a register to an integer.
        reg = self.ram_read(self.pc+1)
        val = self.ram_read(self.pc+2)
        self.registers[reg] = val
        self.pc += 3

    def PRN(self):  # Print numeric value stored in the given register.
        reg = self.ram_read(self.pc+1)
        print(self.registers[reg])
        self.pc += 2

    # Multiply the values in two registers together and store the result in registerA.
    def MUL(self):
        self.alu("MUL", self.pc+1, self.pc+2)

    def PUSH(self):
        # Decrement SP
        # Get the reg num to push
        # Get the value to push
        # Copy the value to the SP address
        # print(memory[0xea:0xf4])
        self.registers[self.sp] -= 1
        reg_number = self.ram[self.pc+1]
        value = self.registers[reg_number]
        self.ram[self.registers[self.sp]] = value
        self.pc += 2

    # Pop the value at the top of the stack into the given register.
    def POP(self):
        # Get reg to pop into
        # Get the top of stack addr
        # top_of_stack_addr = registers[self.sp]
        # Get the value at the top of the stack
        # Store the value in the register
        # Increment the SP
        address = self.registers[self.sp]
        value = self.ram[address]
        self.registers[self.ram[self.pc+1]] = value
        self.registers[self.sp] += 1
        self.pc += 2

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            command = self.ram_read(self.pc)
            if command in self.branch_table:
                self.branch_table[command]()
