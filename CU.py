import tkinter as tk
import math

modules = [('load', 0), ('原码乘法', 1)]
bit = 4
bit10 = (1 << 4)


# 4位寄存器

def list2str(x: list) -> str:
    r = ''
    for i in x:
        r = r + str(i)
    return r


def str2list(x: str) -> list:
    r = [0 for i in range(bit + 1)]
    for i in range(bit + 1):
        r[i] = ord(x[i]) - ord('0')
    return r


def flip(textArea: tk.Text, x: list) -> list:
    textArea.insert(tk.END, '翻转 ' + list2str(x) + '\n')
    for i in range(1, bit + 1):
        x[i] ^= 1
    textArea.insert(tk.END, '翻转完成 ' + list2str(x) + '\n')
    return x


def add(textArea: tk.Text, x: list, y: list) -> list:
    textArea.insert(tk.END, '相加 ' + list2str(x) + ' ' + list2str(y) + '\n')
    curSum = 0
    for i in range(bit, -1, -1):
        x[i] += curSum + y[i]
        curSum = x[i] >> 1
        x[i] %= 2
    textArea.insert(tk.END, '相加结果为: ' + list2str(x) + '\n')
    return x


def load(textArea: tk.Text, config: tk.Variable, input1: str, input2: str) -> [str, str]:
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


def logic_left_shift(textArea: tk.Text, x: list) -> list:
    textArea.insert(tk.END, '逻辑左移 ' + list2str(x) + '\n')
    for i in range(1, bit + 1):
        x[i - 1] = x[i]
    x[bit] = 0
    textArea.insert(tk.END, '逻辑左移完成 ' + list2str(x) + '\n')
    return x


def logic_right_shift(textArea: tk.Text, x: list) -> list:
    textArea.insert(tk.END, '逻辑右移 ' + list2str(x) + '\n')
    for i in range(bit, 0, -1):
        x[i] = x[i - 1]
    x[0] = 0
    textArea.insert(tk.END, '逻辑右移完成 ' + list2str(x) + '\n')
    return x


def arithmetic_left_shift(textArea: tk.Text, x: list) -> list:
    textArea.insert(tk.END, '算数左移 ' + list2str(x) + '\n')
    pass


def arithmetic_right_shift(textArea: tk.Text, x: list) -> list:
    textArea.insert(tk.END, '算数右移 ' + list2str(x) + '\n')
    pass


def raw_mul(textArea: tk.Text, config: tk.Variable, input1: str, input2: str) -> [str, str]:
    [R1, R2] = load(textArea, config, input1, input2)
    textArea.insert(tk.END, '原码一位乘 ' + R1 + ' ' + R2 + '\n')
    R1 = str2list(R1)
    R2 = str2list(R2)
    flag = R1[0] ^ R2[0]
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
    return [list2str(partial_sum), list2str(R2)]


def calc(textArea: tk.Text, config: tk.Variable, input1: str, input2: str) -> [str, str]:
    if config == 0:
        return load(textArea, config, input1, input2)
    if config == 1:
        return raw_mul(textArea, config, input1, input2)
    return ['12', '23']
