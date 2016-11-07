#!/usr/bin/python
from collections import Counter

# Dict of english letters frequency
# Source data http://norvig.com/mayzner.html
ENGLISH_LETTER_FREQUENCY = {
    'E': 0.1249,
    'T': 0.0928,
    'A': 0.0804,
    'O': 0.0764,
    'I': 0.0757,
    'N': 0.0723,
    'S': 0.0651,
    'R': 0.0628,
    'H': 0.0505,
    'L': 0.0407,
    'D': 0.0382,
    'C': 0.0334,
    'U': 0.0273,
    'M': 0.0251,
    'F': 0.024,
    'P': 0.0214,
    'G': 0.0187,
    'W': 0.0168,
    'Y': 0.0166,
    'B': 0.0148,
    'V': 0.0105,
    'K': 0.0054,
    'X': 0.0023,
    'J': 0.0016,
    'Q': 0.0012,
    'Z': 0.0009,
}

# Threshold to count char sequence as english text
# Got by trial and error
ENGLISH_TEXT_THRESHOLD = 0.045

MOST_FREQUENT_CHARS = 'ETAOIN SRHLDCU'


def is_english_text(arr):
    """
    Try to define if this text is english
    Count alphabet_index as sum of probability of all letters
    Then divide this index on arr len and compare with threshold
    """
    alphabet_index = 0.0
    for char in arr:
        alphabet_index += ENGLISH_LETTER_FREQUENCY.get(chr(char).upper(), 0.0)
    return (alphabet_index / len(arr)) >= ENGLISH_TEXT_THRESHOLD


def try_to_decipher(seq):
    """
    * Convert hex to bytearray
    * Get list of byte tuples by usage frequency
    * Try to guess what char from most frequently used was encrypted by simple
    brute force
    * Check every response if it is valid string
    """
    arr = bytearray.fromhex(seq)
    ordered = Counter(arr).most_common(1)

    for char in MOST_FREQUENT_CHARS:
        key = ordered[0][0] ^ ord(char)
        result = bytearray(item ^ key for item in arr)
        if is_english_text(result):
            return result


def find_enciphered_lines(filename):
    """
    Read file line by line and try to decipher
    If deciphered line looks like english text
    yield line num and deciphered text
    """
    with open(filename, 'r') as f:
        for num, line in enumerate(f):
            result = try_to_decipher(line.strip())
            if result:
                yield num, result


#########
# TESTS #
#########
def test_is_english_text():
    return is_english_text(bytearray('some english text')) and\
           not is_english_text(bytearray('zzz == !'))


def test_find_enciphered_lines():
    deciphered_lines = list(find_enciphered_lines('4.txt'))
    if len(deciphered_lines) != 1:
        return False
    if deciphered_lines[0][0] != 170:
        return False
    return deciphered_lines[0][1] == bytearray('Now that the party is jumping\n')


if __name__ == "__main__":
    for name, obj in globals().items():
        if name.startswith('test_'):
            print ('\033[1;32m.\033[1;m' if obj() else '\033[1;31mX\033[1;m'),
