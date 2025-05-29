def convert(hlasm_code):
    lines = hlasm_code.strip().splitlines()
    consts = {}
    labels = {}
    variables = {}
    strings = {}
    program = []
    bytecode = []
    pc = 0
    data_start = 512

    for line in lines:
        line = line.strip().split(';')[0]
        if not line:
            continue
        if line.startswith(".const"):
            _, name, value = line.split()
            consts[name] = int(value)
        elif line.startswith(".string"):
            _, name, value = line.split(maxsplit=2)
            strings[name] = [ord(c) for c in value.strip('"')]
        elif line.startswith(".var"):
            _, name = line.split()
            variables[name] = None
        elif line.endswith(":"):
            labels[line[:-1]] = pc
        else:
            inst = line.split()[0]
            pc += (
                5 if inst in ["LDA", "ADD", "SUB", "MUL", "DIV"] else
                3 if inst in ["JMP", "RET"] else
                7 if inst in ["JIE", "JIL", "JIG"] else
                23 if inst == "CALL" else
                1
            )
            program.append(line)

    current_addr = pc + data_start
    for name in variables:
        variables[name] = current_addr
        current_addr += 1
    for name, chars in strings.items():
        variables[name] = current_addr
        current_addr += len(chars)

    def resolve(value):
        if value in consts:
            return consts[value]
        elif value in variables:
            return variables[value]
        elif value in labels:
            return labels[value] + data_start
        else:
            return int(value)

    for line in program:
        tokens = line.split()
        inst = tokens[0]

        if inst == "HLT":
            bytecode.append(0)
        elif inst in ["LDA", "ADD", "SUB", "MUL", "DIV"]:
            a, b = resolve(tokens[1]), resolve(tokens[2])
            opcode = {"LDA": 1, "ADD": 2, "SUB": 3, "MUL": 4, "DIV": 5}[inst]
            bytecode.extend([opcode, a // 256, a % 256, b // 256, b % 256])
        elif inst == "JMP":
            j = resolve(tokens[1])
            bytecode.extend([6, j // 256, j % 256])
        elif inst in ["JIE", "JIL", "JIG"]:
            j, c, d = resolve(tokens[3]), resolve(tokens[1]), resolve(tokens[2])
            opcode = {"JIE": 7, "JIL": 8, "JIG": 9}[inst]
            bytecode.extend([opcode, j // 256, j % 256, c // 256, c % 256, d // 256, d % 256])
        elif inst == "CALL":
            label_addr = resolve(tokens[1])
            ret_addr = len(bytecode) + 23
            tmp = 59990
            sp_addr = 60000
            bytecode.extend([
                1, ret_addr // 256, ret_addr % 256, tmp // 256, tmp % 256,
                1, sp_addr // 256, sp_addr % 256, (tmp+1) // 256, (tmp+1) % 256,
                2, tmp // 256, tmp % 256, (tmp+1) // 256, (tmp+1) % 256,
                1, tmp // 256, tmp % 256, (tmp+2) // 256, (tmp+2) % 256,
                1, (tmp+1) // 256, (tmp+1) % 256, (tmp+3) // 256, (tmp+3) % 256,
                2, (tmp+2) // 256, (tmp+2) % 256, (tmp+3) // 256, (tmp+3) % 256,
                1, sp_addr // 256, sp_addr % 256, (tmp+4) // 256, (tmp+4) % 256,
                2, 0, 1, (tmp+4) // 256, (tmp+4) % 256,
                1, (tmp+4) // 256, (tmp+4) % 256, sp_addr // 256, sp_addr % 256,
                6, label_addr // 256, label_addr % 256
            ])
        elif inst == "RET":
            tmp = 59990
            sp_addr = 60000
            bytecode.extend([
                1, sp_addr // 256, sp_addr % 256, tmp // 256, tmp % 256,
                3, 0, 1, tmp // 256, tmp % 256,
                1, tmp // 256, tmp % 256, sp_addr // 256, sp_addr % 256,
                1, tmp // 256, tmp % 256, (tmp+1) // 256, (tmp+1) % 256,
                6, 0, 0
            ])
    return bytecode
f_name = input('What file do you want to compile? ')
with open(f_name).read() as f:
    print(str(convert(f)))