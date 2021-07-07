memory = [
    1,  # print beej
    1,  # print beej
    1,  # print beej
    2,  # halt
]


pc = 0  # Program Counter, address of the currently executing instruction
running = True

while running:
    ir = memory[pc]
    if ir == 1:
        print("Beej")
        pc += 1
    elif ir == 2:
        running = False
    else:
        print("Unknown Instruction Given")
