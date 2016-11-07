#!/usr/bin/python
import binascii
from itertools import izip


def xor_hex(value1, value2):
    if len(value1) != len(value2):
        return
    b_array1 = bytearray.fromhex(value1)
    b_array2 = bytearray.fromhex(value2)
    result = bytearray(x ^ y for x, y in izip(b_array1, b_array2))
    return binascii.hexlify(result)


def test_xor_hex():
    hex1 = '1c0111001f010100061a024b53535009181c'
    hex2 = '686974207468652062756c6c277320657965'
    expected_hex = '746865206b696420646f6e277420706c6179'
    return expected_hex == xor_hex(hex1, hex2)


def test_xor_hex_wrong_len():
    hex1 = '1c0111001'
    hex2 = '1c011100'
    return xor_hex(hex1, hex2) is None


if __name__ == "__main__":
    for name, obj in globals().items():
        if name.startswith('test_'):
            print ('\033[1;32m.\033[1;m' if obj() else '\033[1;31mX\033[1;m'),
