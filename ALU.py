import tkinter as tk
from typing import TypeVar

_bit_ = 4

T = TypeVar('T', bound='Register')


class Register(object):
    def __init__(self, bit_length: int):
        self.bit_length = bit_length
        self.bit_capacity = self.bit_length + 2
        self.bit_array = [0 for _ in range(self.bit_capacity)]

    def __getitem__(self, item: int) -> int:
        return self.bit_array[item]

    def get_number_flag(self):
        return self.bit_array[self.bit_capacity - 1]

    def __setitem__(self, key: int, value: int):
        self.bit_array[key] = value

    def set_by_ratio(self, x: int):
        upper = (1 << self.bit_length) - 1
        bound = -(1 << self.bit_length)
        if x > upper or x < bound:
            raise Exception
        if x < 0:
            flag = 1
            self[self.bit_capacity - 1] = self[self.bit_capacity - 2] = 1
            x = -x
        else:
            flag = 0
        for i in range(self.bit_length):
            self[i] = (x & 1)
            x >>= 1
        if flag == 1:
            self.flip_partial()
            o = Register(self.bit_length)
            o[0] = 1
            self.add(o)
            self[self.bit_capacity - 1] = self[self.bit_capacity - 2] = 1

    def set_by_binary_string(self, content: str):
        if content is None or len(content) != self.bit_capacity:
            raise Exception
        for i in range(self.bit_capacity):
            self.bit_array[i] = ord(content[self.bit_capacity - i - 1]) - ord('0')

    def to_binary_string(self) -> str:
        binary_string = ""
        for i in range(self.bit_capacity):
            binary_string += str(self.bit_array[self.bit_capacity - i - 1])
        return binary_string

    def logistic_left_shift(self):
        for i in range(self.bit_capacity - 1, 0, -1):
            self.bit_array[i] = self.bit_array[i - 1]
        self.bit_array[0] = 0

    def logistic_right_shift(self):
        for i in range(0, self.bit_capacity - 1):
            self.bit_array[i] = self.bit_array[i + 1]
        self.bit_array[self.bit_capacity - 1] = 0

    def arithmetic_right_shift(self):
        for i in range(0, self.bit_capacity - 1):
            self.bit_array[i] = self.bit_array[i + 1]

    def arithmetic_left_shift(self):
        for i in range(self.bit_capacity - 3, 0, -1):
            self.bit_array[i] = self.bit_array[i - 1]
        self.bit_array[0] = 0

    def flip_all(self):
        for i in range(self.bit_capacity):
            self.bit_array[i] = 1 - self.bit_array[i]

    def flip_partial(self):
        for i in range(self.bit_capacity - 1):
            self.bit_array[i] = 1 - self.bit_array[i]

    def add(self, o: T):
        if o.bit_capacity != self.bit_capacity:
            raise Exception
        partial_sum = 0
        for i in range(self.bit_capacity):
            partial_sum += self.bit_array[i] + o.bit_array[i]
            self.bit_array[i] = partial_sum % 2
            partial_sum >>= 1

    def convert_complement_ratio(self) -> int:
        if self.bit_array[self.bit_capacity - 1] == 0:
            return self.convert_raw_ratio()
        o = Register(self.bit_length)
        o.flip_all()
        o.add(self)
        o.flip_partial()
        return o.convert_raw_ratio()

    def convert_raw_ratio(self) -> int:
        if self.bit_array[self.bit_capacity - 1] == 0:
            flag = 1
        else:
            flag = -1
        partial_sum = 0
        for i in range(self.bit_length - 1, -1, -1):
            partial_sum <<= 1
            partial_sum |= self.bit_array[i]
        return flag * partial_sum
