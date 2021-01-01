import tkinter as tk
import math

modules = [('load', 0), ('原码乘法', 1), ('补码乘法', 2)]
_bit_ = 4
bit10 = (1 << 4)


# 4位寄存器

def list2str(x: list) -> str:
    r = ''
    for i in x:
        r = r + str(i)
    return r


def str2list(x: str, bit=_bit_) -> list:
    r = [0 for i in range(bit + 1)]
    for i in range(bit + 1):
        r[i] = ord(x[i]) - ord('0')
    return r


def flip(textArea: tk.Text, x: list, bit=_bit_) -> list:
    textArea.insert(tk.END, '翻转 ' + list2str(x) + '\n')
    for i in range(1, bit + 1):
        x[i] ^= 1
    textArea.insert(tk.END, '翻转完成 ' + list2str(x) + '\n')
    return x


def add(textArea: tk.Text, x: list, y: list, bit=_bit_) -> list:
    textArea.insert(tk.END, '相加 ' + list2str(x) + ' ' + list2str(y) + '\n')
    curSum = 0
    for i in range(bit, -1, -1):
        x[i] += curSum + y[i]
        curSum = x[i] >> 1
        x[i] %= 2
    textArea.insert(tk.END, '相加结果为: ' + list2str(x) + '\n')
    return x


def load(textArea: tk.Text, config: tk.Variable, input1: str, input2: str, bit=_bit_) -> [str, str]:
    number = int(input1)
    number2 = int(input2)
    n2um1 = [0 for i in range(bit + 1)]
    n2um2 = [0 for i in range(bit + 1)]
    if number < 0:
        n2um1[0] = 1
        number = -number
    if number2 < 0:
        n2um2[0] = 1
        number2 = -number2

    t = 1
    while t <= bit:
        n2um1[bit + 1 - t] = (number % 2)
        number >>= 1
        n2um2[bit + 1 - t] = (number2 % 2)
        number2 >>= 1
        t += 1
    textArea.insert(tk.END, '获得原码\n')
    textArea.insert(tk.END, list2str(n2um1) + '\n')
    textArea.insert(tk.END, list2str(n2um2) + '\n')

    if n2um1[0] == 1:
        n2um1 = flip(textArea, n2um1)
        tmp = [0 for i in range(bit + 1)]
        tmp[bit] = 1
        n2um1 = add(textArea, n2um1, tmp)
        n2um1[0] = 1
    if n2um2[0] == 1:
        n2um2 = flip(textArea, n2um2)
        tmp = [0 for i in range(bit + 1)]
        tmp[bit] = 1
        n2um2 = add(textArea, n2um2, tmp)
        n2um2[0] = 1

    return [list2str(n2um1), list2str(n2um2)]
def load_raw(textArea: tk.Text, config: tk.Variable, input1: str, input2: str, bit=_bit_) -> [str, str]:
    number = int(input1)
    number2 = int(input2)
    n2um1 = [0 for i in range(bit + 1)]
    n2um2 = [0 for i in range(bit + 1)]
    if number < 0:
        n2um1[0] = 1
        number = -number
    if number2 < 0:
        n2um2[0] = 1
        number2 = -number2

    t = 1
    while t <= bit:
        n2um1[bit + 1 - t] = (number % 2)
        number >>= 1
        n2um2[bit + 1 - t] = (number2 % 2)
        number2 >>= 1
        t += 1
    textArea.insert(tk.END, '获得原码\n')
    textArea.insert(tk.END, list2str(n2um1) + '\n')
    textArea.insert(tk.END, list2str(n2um2) + '\n')
    return [list2str(n2um1), list2str(n2um2)]


def logic_left_shift(textArea: tk.Text, x: list, bit=_bit_) -> list:
    textArea.insert(tk.END, '逻辑左移 ' + list2str(x) + '\n')
    for i in range(1, bit + 1):
        x[i - 1] = x[i]
    x[bit] = 0
    textArea.insert(tk.END, '逻辑左移完成 ' + list2str(x) + '\n')
    return x


def logic_right_shift(textArea: tk.Text, x: list, bit=_bit_) -> list:
    textArea.insert(tk.END, '逻辑右移 ' + list2str(x) + '\n')
    for i in range(bit, 0, -1):
        x[i] = x[i - 1]
    x[0] = 0
    textArea.insert(tk.END, '逻辑右移完成 ' + list2str(x) + '\n')
    return x


def arithmetic_left_shift(textArea: tk.Text, x: list, bit=_bit_) -> list:
    textArea.insert(tk.END, '补码算数左移 ' + list2str(x) + '\n')
    for i in range(1, bit):
        x[i] = x[i+1]
    x[bit + 1] = 0
    textArea.insert(tk.END, '补码算数左移完成 ' + list2str(x) + '\n')
    return x


def arithmetic_right_shift(textArea: tk.Text, x: list, bit=_bit_) -> list:
    textArea.insert(tk.END, '补码算数右移 ' + list2str(x) + '\n')
    for i in range(bit, 0, -1):
        x[i] = x[i-1]
    textArea.insert(tk.END, '补码算数右移完成 ' + list2str(x) + '\n')
    return x


def raw_mul(textArea: tk.Text, config: tk.Variable, input1: str, input2: str, bit=_bit_) -> [str, str]:
    [R1, R2] = load_raw(textArea, config, input1, input2)
    textArea.insert(tk.END, '原码一位乘 ' + R1 + ' ' + R2 + '\n')
    R1 = str2list(R1)
    R2 = str2list(R2)
    flag = R1[0] ^ R2[0]
    R1[0] = R2[0] = 0
    textArea.insert(tk.END, '确定符号位 ' + str(flag) + '\n')
    partial_sum = [0 for i in range(bit + 1)]
    for i in range(bit):
        if R2[bit] == 1:
            textArea.insert(tk.END, '寄存器最后一位为1 加\n')
            partial_sum = add(textArea, partial_sum, R1)
        textArea.insert(tk.END, '寄存器与部分和右移\n')
        textArea.insert(tk.END, '寄存器')
        R2 = logic_right_shift(textArea, R2)
        R2[1] = partial_sum[bit]
        textArea.insert(tk.END, '部分和')
        partial_sum = logic_right_shift(textArea, partial_sum)
        textArea.insert(tk.END, '部分和 ' + list2str(partial_sum) + ' 寄存器' + list2str(R2) + '\n')
    partial_sum[0] = flag
    textArea.insert(tk.END, '原码一位乘结果为 ' + list2str(partial_sum))
    for i in range(1, bit+1):
        textArea.insert(tk.END, str(R2[i]))
    textArea.insert(tk.END, '\n')
    return [list2str(partial_sum), list2str(R2)]


def complement_mul(textArea: tk.Text, config: tk.Variable, input1: str, input2: str, bit=_bit_) -> [str, str]:
    [R1, R2] = load(textArea, config, input1, input2)
    R1 = str2list(R1)
    R2 = str2list(R2)
    R1.insert(0, R1[0])
    R2.insert(0, R2[0])
    textArea.insert(tk.END, '扩容成双符号位 ' + list2str(R1) + ' ' + list2str(R2) + '\n')
    R3 = str2list(load(textArea, config, input1, str(-int(input1)))[1])
    R3.insert(0, R3[0])
    textArea.insert(tk.END, '得到被乘数加法逆元的补码 ' + list2str(R3) + '\n')
    textArea.insert(tk.END, '添加末尾0\n')
    R2 = logic_left_shift(textArea, R2, bit + 1)
    partial_sum = [0 for i in range(bit + 2)]
    for i in range(bit + 1):
        flag = R2[bit+1] - R2[bit]
        textArea.insert(tk.END, '寄存器的尾数为 ' + str(R2[bit]) + ' ' + str(R2[bit+1]) + '\n')
        textArea.insert(tk.END, '当前状态为 ' + str(flag) + '\n')
        if flag == 1:
            partial_sum = add(textArea, partial_sum, R1, bit + 1)
        elif flag == -1:
            partial_sum = add(textArea, partial_sum, R3, bit + 1)
        if i != bit:
            R2 = logic_right_shift(textArea, R2, bit + 1)
            R2[0] = partial_sum[bit + 1]
            partial_sum = arithmetic_right_shift(textArea, partial_sum, bit + 1)
        textArea.insert(tk.END, '部分和 ' + list2str(partial_sum) + '寄存器 ' + list2str(R2) + '\n')
    textArea.insert(tk.END, '补码一位乘结果为 ' + list2str(partial_sum))
    for i in range(bit):
        textArea.insert(tk.END, R2[i])
    textArea.insert(tk.END, '\n')
    return [list2str(partial_sum), list2str(R2)]


def calc(textArea: tk.Text, config: tk.Variable, input1: str, input2: str) -> [str, str]:
    if config == 0:
        return load(textArea, config, input1, input2)
    if config == 1:
        return raw_mul(textArea, config, input1, input2)
    if config == 2:
        return complement_mul(textArea, config, input1, input2)
    return ['12', '23']
