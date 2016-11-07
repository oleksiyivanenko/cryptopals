#!/usr/bin/python
"""
Cryptopals set 1 challenge 1

Convert hex to base64

The string:
49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d
Should produce:
SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
"""

import base64


def hex_to_base64(value):
    return base64.b64encode(bytearray.fromhex(value))


def test_hex_to_base64():
    hex_str = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    expected_base64 = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    return expected_base64 == hex_to_base64(hex_str)


if __name__ == "__main__":
    for name, obj in globals().items():
        if name.startswith('test_'):
            print ('\033[1;32m.\033[1;m' if obj() else '\033[1;31mX\033[1;m'),
