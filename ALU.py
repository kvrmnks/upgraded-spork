import tkinter as tk

_bit_ = 4


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


# 不翻转第一位
def flip(textArea: tk.Text, x: list) -> list:
    textArea.insert(tk.END, '翻转 ' + list2str(x) + '\n')
    for i in range(1, len(x)):
        x[i] ^= 1
    textArea.insert(tk.END, '翻转完成 ' + list2str(x) + '\n')
    return x


# 全部参与运算
def add(textArea: tk.Text, x: list, y: list) -> list:
    textArea.insert(tk.END, '相加 ' + list2str(x) + ' ' + list2str(y) + '\n')
    curSum = 0
    for i in range(len(x)-1, -1, -1):
        x[i] += curSum + y[i]
        curSum = x[i] >> 1
        x[i] %= 2
    textArea.insert(tk.END, '相加结果为: ' + list2str(x) + '\n')
    return x


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
        x[i] = x[i + 1]
    x[bit + 1] = 0
    textArea.insert(tk.END, '补码算数左移完成 ' + list2str(x) + '\n')
    return x


def arithmetic_right_shift(textArea: tk.Text, x: list, bit=_bit_) -> list:
    textArea.insert(tk.END, '补码算数右移 ' + list2str(x) + '\n')
    for i in range(bit, 0, -1):
        x[i] = x[i - 1]
    textArea.insert(tk.END, '补码算数右移完成 ' + list2str(x) + '\n')
    return x


def load_raw(textArea: tk.Text, x: str, bit=_bit_) -> list:
    number = int(x)
    n2um1 = [0 for i in range(bit + 1)]
    if number < 0:
        n2um1[0] = 1
        number = -number
    t = 1
    while t <= bit:
        n2um1[bit + 1 - t] = (number % 2)
        number >>= 1
        t += 1
    textArea.insert(tk.END, '获得原码\n')
    textArea.insert(tk.END, list2str(n2um1) + '\n')
    return n2um1


def load_complement(textArea: tk.Text, x: str, bit=_bit_) -> list:
    n2um = load_raw(textArea, x, bit)
    if n2um[0] == 1:
        n2um = flip(textArea, n2um)
        tmp = [0 for i in range(bit + 1)]
        tmp[bit] = 1
        n2um = add(textArea, n2um, tmp)
        n2um[0] = 1
    textArea.insert(tk.END, '获得补码')
    textArea.insert(tk.END, list2str(n2um) + '\n')
    return n2um


def complement_list2number_1flag(textArea: tk.Text, x: list) -> int:
    textArea.insert(tk.END, '将2进制补码转为10进制 ' + list2str(x) + '\n')
    if x[0] == 1:
        tmp = [1 for i in range(len(x))]
        x = add(textArea, x, tmp)
        x = flip(textArea, x)
        x.pop(0)
        number = -int(list2str(x), 2)
    else:
        x.pop(0)
        number = int(list2str(x), 2)
    textArea.insert(tk.END, '结果为 ' + str(number) + '\n')
    return number


def complement_list2number_2flag(textArea: tk.Text, x: list) -> int:
    x.pop(0)
    return complement_list2number_1flag(textArea, x)


def raw_list2number_1flag(textArea: tk.Text, x: list) -> int:
    textArea.insert(tk.END, '将2进制原码转为10进制 ' + list2str(x) + '\n')
    if x[0] == 0:
        flag = 1
    else:
        flag = -1
    x.pop(0)
    number = flag * int(list2str(x), 2)
    textArea.insert(tk.END, '结果为 ' + str(number) + '\n')
    return number


def raw_list2number_2flag(textArea: tk.Text, x: list) -> int:
    x.pop(0)
    return raw_list2number_1flag(textArea, x)
