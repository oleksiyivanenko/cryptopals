#!/usr/bin/python
import string
from collections import Counter

MOST_FREQUENT_CHARS = 'ETAOIN SHRDLU'


def get_by_frequency(arr):
    """
    Return list of tuples in order of usage frequency in arr
    First tuple element - element from arr
    Second tuple element - usages number
    E.g.: [('a', 3), ('b', 2), ('c', 1)]
    """
    return Counter(arr).most_common()


def is_valid_chars(arr):
    """
    Expected bytearray on input
    Try to convert first several bytes to chars and check
    if they in ascii_letters
    If all of them ascii - return True
    """
    TEST_TO_INDEX = 3
    return all([chr(item) in string.ascii_letters for item in arr[:TEST_TO_INDEX]])


def try_to_decipher(seq):
    """
    * Convert hex to bytearray
    * Get list of byte tuples by usage frequency
    * Try to guess what char from most frequently used was encrypted by simple
    brute force
    * Check every response if it is valid string
    """
    arr = bytearray.fromhex(seq)
    ordered = get_by_frequency(arr)

    for char in MOST_FREQUENT_CHARS:
        key = ordered[0][0] ^ ord(char)
        result = bytearray(item ^ key for item in arr)
        if is_valid_chars(result):
            return result


#########
# TESTS #
#########
def test_get_by_frequency():
    arr = 'cbbaaa'
    expected = [('a', 3), ('b', 2), ('c', 1)]
    return expected == get_by_frequency(arr)


def test_is_valid_chars():
    return is_valid_chars(bytearray('Some')) and not is_valid_chars(bytearray('=['))


def test_try_to_decipher():
    encoded = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    expected = "Cooking MC's like a pound of bacon"
    return expected == try_to_decipher(encoded)

if __name__ == "__main__":
    for name, obj in globals().items():
        if name.startswith('test_'):
            print ('\033[1;32m.\033[1;m' if obj() else '\033[1;31mX\033[1;m'),
