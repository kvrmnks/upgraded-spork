from ALU import *
import math

modules = [('load', 0), ('原码乘法', 1), ('补码乘法', 2)]

# 4位寄存器
_bit_ = 4
bit10 = (1 << 4)


def load(textArea: tk.Text, config: tk.Variable, input1: str, input2: str, bit=_bit_) -> [str, str]:
    n2um1 = load_complement(textArea, input1, bit)
    n2um2 = load_complement(textArea, input2, bit)
    return [list2str(n2um1), list2str(n2um2)]


def raw_mul(textArea: tk.Text, config: tk.Variable, input1: str, input2: str, bit=_bit_) -> [str, str]:
    R1 = load_raw(textArea, input1, bit)
    R2 = load_raw(textArea, input2, bit)
    textArea.insert(tk.END, '原码一位乘 ' + list2str(R1) + ' ' + list2str(R2) + '\n')
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
    ans = partial_sum.copy()
    textArea.insert(tk.END, '原码一位乘结果为 ' + list2str(partial_sum))
    for i in range(1, bit + 1):
        textArea.insert(tk.END, str(R2[i]))
        ans.append(R2[i])
    textArea.insert(tk.END, '\n')
    raw_list2number_1flag(textArea, ans)
    return [list2str(partial_sum), list2str(R2)]


def complement_mul(textArea: tk.Text, config: tk.Variable, input1: str, input2: str, bit=_bit_) -> [str, str]:
    R1 = load_complement(textArea, input1, bit)
    R2 = load_complement(textArea, input2, bit)
    R1.insert(0, R1[0])
    R2.insert(0, R2[0])
    textArea.insert(tk.END, '扩容成双符号位 ' + list2str(R1) + ' ' + list2str(R2) + '\n')
    R3 = load_complement(textArea, str(-int(input1)), bit)
    R3.insert(0, R3[0])
    textArea.insert(tk.END, '得到被乘数加法逆元的补码 ' + list2str(R3) + '\n')
    textArea.insert(tk.END, '添加末尾0\n')
    R2 = logic_left_shift(textArea, R2, bit + 1)
    partial_sum = [0 for i in range(bit + 2)]
    for i in range(bit + 1):
        flag = R2[bit + 1] - R2[bit]
        textArea.insert(tk.END, '寄存器的尾数为 ' + str(R2[bit]) + ' ' + str(R2[bit + 1]) + '\n')
        textArea.insert(tk.END, '当前状态为 ' + str(flag) + '\n')
        if flag == 1:
            partial_sum = add(textArea, partial_sum, R1)
        elif flag == -1:
            partial_sum = add(textArea, partial_sum, R3)
        if i != bit:
            R2 = logic_right_shift(textArea, R2, bit + 1)
            R2[0] = partial_sum[bit + 1]
            partial_sum = arithmetic_right_shift(textArea, partial_sum, bit + 1)
        textArea.insert(tk.END, '部分和 ' + list2str(partial_sum) + '寄存器 ' + list2str(R2) + '\n')
    ans = partial_sum.copy()
    textArea.insert(tk.END, '补码一位乘结果为 ' + list2str(partial_sum))
    for i in range(bit):
        textArea.insert(tk.END, R2[i])
        ans.append(R2[i])
    textArea.insert(tk.END, '\n')
    complement_list2number_2flag(textArea, ans)
    return [list2str(partial_sum), list2str(R2)]


def calc(textArea: tk.Text, config: tk.Variable, input1: str, input2: str) -> [str, str]:
    if config == 0:
        return load(textArea, config, input1, input2)
    if config == 1:
        return raw_mul(textArea, config, input1, input2)
    if config == 2:
        return complement_mul(textArea, config, input1, input2)
    return ['12', '23']
