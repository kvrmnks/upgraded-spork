from ALU import *

modules = [('输入', 0), ('原码乘法', 1), ('补码乘法', 2), ('IEEE754解析', 3), ('浮点数转IEEE754', 4)]
register_modules = [('RAX', 0), ('RBX', 1), ('RCX', 2), ('RDX', 3)]
REGISTER = [Register(1), Register(1), Register(1), Register(1)]


def covert_complement_to_raw(RX: Register):
    o = Register(RX.bit_length)
    for i in range(RX.bit_capacity):
        o[i] = 1
    RX.add(o)
    RX.flip_partial()
    RX[RX.bit_capacity - 2] = RX[RX.bit_capacity - 1]


def load(textArea: tk.Text, registerConfig: int, input1: str, bit_length: int) -> []:
    input1 = int(input1)
    textArea.insert(tk.END, '加载' + str(input1) + '到' + register_modules[registerConfig][0] + '\n')
    REGISTER[registerConfig] = Register(bit_length)
    REGISTER[registerConfig].set_by_ratio(input1)
    yield [x.to_binary_string() for x in REGISTER]


def raw_mul(textArea: tk.Text) -> []:
    RAX, RBX, RCX = REGISTER[0], REGISTER[1], REGISTER[2]
    if RAX.bit_capacity != RBX.bit_capacity:
        raise Exception
    else:
        RCX = REGISTER[2] = Register(RAX.bit_length)

    textArea.insert(tk.END, '原码一位乘 \n')

    flag = RAX.get_number_flag() ^ RBX.get_number_flag()

    if RAX[RAX.bit_capacity - 1] == 1:
        covert_complement_to_raw(RAX)
    if RBX[RBX.bit_capacity - 1] == 1:
        covert_complement_to_raw(RBX)
    RBX.logistic_left_shift()
    RBX.logistic_left_shift()
    textArea.insert(tk.END, '确定符号位 ' + str(flag) + '\n')
    yield [x.to_binary_string() for x in REGISTER]

    for i in range(RBX.bit_length):
        if RBX[2] == 1:
            textArea.insert(tk.END, '寄存器最后一位为1 加\n')
            RCX.add(RAX)
        textArea.insert(tk.END, '寄存器与部分和右移\n')
        textArea.insert(tk.END, '寄存器')
        RBX.logistic_right_shift()
        RBX[RBX.bit_capacity - 1] = RCX[0]
        RCX.logistic_right_shift()
        textArea.insert(tk.END, '部分和 ' + RCX.to_binary_string() + '\n')
        yield [x.to_binary_string() for x in REGISTER]

    RCX[RCX.bit_capacity - 1] = RCX[RCX.bit_capacity - 2] = flag
    o = RCX.to_binary_string()
    for i in range(RBX.bit_capacity - 1, 1, -1):
        o += str(RBX[i])
    p = Register(2 * RAX.bit_length)
    p.set_by_binary_string(o)
    textArea.insert(tk.END, '原码一位乘结果为 ' + p.to_binary_string() + '\n 值为 ' + str(p.convert_raw_ratio()))

    yield [x.to_binary_string() for x in REGISTER]


def complement_mul(textArea: tk.Text) -> []:
    RAX, RBX, RCX, RDX = REGISTER[0], REGISTER[1], REGISTER[2], REGISTER[3]
    if RAX.bit_capacity != RBX.bit_capacity:
        raise Exception
    else:
        RCX = REGISTER[2] = Register(RAX.bit_length)
        RDX = REGISTER[3] = Register(RAX.bit_length)

    RDX.set_by_ratio(-RAX.convert_complement_ratio())
    textArea.insert(tk.END, '得到被乘数加法逆元的补码 ' + RDX.to_binary_string() + '\n')
    textArea.insert(tk.END, '添加末尾0\n')

    RBX.logistic_left_shift()
    yield [x.to_binary_string() for x in REGISTER]

    for i in range(RAX.bit_length + 1):
        flag = RBX[0] - RBX[1]
        textArea.insert(tk.END, '寄存器的尾数为 ' + str(RBX[0]) + ' ' + str(RBX[1]) + '\n')
        textArea.insert(tk.END, '当前状态为 ' + str(flag) + '\n')
        if flag == 1:
            textArea.insert(tk.END, '部分和加RAX\n')
            RCX.add(RAX)
        elif flag == -1:
            textArea.insert(tk.END, '部分和加负RAX\n')
            RCX.add(RDX)
        if i != RAX.bit_length:
            textArea.insert(tk.END, '部分和与RBX右移\n')
            RBX.logistic_right_shift()
            RBX[RBX.bit_capacity - 1] = RCX[0]
            RCX.arithmetic_right_shift()

        yield [x.to_binary_string() for x in REGISTER]

    o = RCX.to_binary_string()
    for i in range(RBX.bit_capacity - 1, 1, -1):
        o += str(RBX[i])
    p = Register(2 * RAX.bit_length)
    p.set_by_binary_string(o)
    textArea.insert(tk.END, '补码一位乘结果为 ' + p.to_binary_string() + '\n' + '值为 ' + str(p.convert_complement_ratio()))
    yield [x.to_binary_string() for x in REGISTER]


cu_iter = None


def calc(textArea: tk.Text, config: int, registerConfig: int, input1: str, bit_length: int):
    global cu_iter
    if config == 0:
        cu_iter = load(textArea, registerConfig, input1, bit_length)
    if config == 1:
        cu_iter = raw_mul(textArea)
    if config == 2:
        cu_iter = complement_mul(textArea)


def next_step():
    global cu_iter
    try:
        r = next(cu_iter)
        return r
    except Exception:
        return None
