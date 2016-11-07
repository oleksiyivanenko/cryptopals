#!/usr/bin/python
import binascii
import sys
from collections import Counter
from itertools import izip, tee

MOST_FREQUENT_CHARS = 'ETAOIN SHRDLU'

ENGLISH_LETTER_FREQUENCY = {
    ' ': 0.13,
    'E': 0.12702,
    'T': 0.09056,
    'A': 0.08167,
    'O': 0.07507,
    'I': 0.06966,
    'N': 0.06749,
    'S': 0.06327,
    'H': 0.06094,
    'R': 0.05987,
    'D': 0.04253,
    'L': 0.04025,
    'C': 0.02782,
    'U': 0.02758,
    'M': 0.02406,
    'W': 0.02361,
    'F': 0.02228,
    'G': 0.02015,
    'Y': 0.01974,
    'P': 0.01929,
    'B': 0.01492,
    'V': 0.00978,
    'K': 0.00772,
    'J': 0.00153,
    'X': 0.00150,
    'Q': 0.00095,
    'Z': 0.00074,
}

# Threshold to count char sequence as english text
# Got by trial and error
ENGLISH_TEXT_THRESHOLD = 0.05

MAX_KEYSIZE = 40  # max key length for Vigenere cypher
BLOCKS_TO_COMPARE = 10  # Num of blocks for collecting hamming distance stats


def _pairwise(iterable):
    """
    Make from iterable new iterable by pairs
    "s -> (s0, s1), (s1, s2), (s2, s3) ..."
    """
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


def _repeating_xor(text, key):
    """
    Iterate over every text element and xor it wit key elements
    one by one. In case of text longer than key key will be used
    repeatedly.
    text - text to xor bytes array
    key - key raw bytes array
    returns - bytes array ofter xor
    """
    key_length = len(key)
    result = bytearray(
        char ^ key[index % key_length]
        for index, char in enumerate(text)
    )
    return result


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


def hamming_distance(block1, block2):
    """
    Return hamming distance between two bytes sequences
    Hamming distance - number of bit substitutions required to convert first
    sequence into second
    """
    assert len(block1) == len(block2), 'Blocks must be same length'
    distance = 0
    for char1, char2 in izip(block1, block2):
        distance += bin(char1 ^ char2).count('1')
    return distance


def get_keysize(sequence):
    """
    For every possible keysize up to MAX_KEYSIZE calculate
    average hamming distance between blocks of keysize length.
    Return keysize with smallest distance
    """
    average_distances = []
    for keysize in xrange(2, MAX_KEYSIZE):
        blocks = [sequence[keysize * num: keysize * (num + 1)]
                  for num in xrange(BLOCKS_TO_COMPARE)]
        distances = []
        for pair in _pairwise(blocks):
            distances.append(hamming_distance(*pair))

        average_distances.append((
            (float(sum(distances)) / float(len(distances))) / keysize,
            keysize
        ))

    return min(average_distances)[1]


def get_single_byte_xor_key(seq):
    """
    Decipher singlebyte xor seq and return key
    """
    ordered = Counter(seq).most_common(1)

    for char in MOST_FREQUENT_CHARS:
        key = ordered[0][0] ^ ord(char)
        result = bytearray(item ^ key for item in seq)
        if is_english_text(result):
            return key


def decipher_repeating_xor_file(key, in_file, out_file=None):
    """
    Just decipher in_file with key via repeating xor
    Write result to out_file if provided or to stdout
    """
    file_buffer = bytearray()
    with open(in_file, 'r') as in_f:
        for line in in_f:
            file_buffer.extend(binascii.a2b_base64(line.strip()))

    deciphered_text = _repeating_xor(file_buffer, key)

    if out_file:
        with open('out.txt', 'w') as out_f:
            out_f.write(deciphered_text)
    else:
        sys.stdout.write(deciphered_text)


def break_repeating_xor(in_file):
    """
    * Read encrypted file to buffer
    * Guess keysize
    * Get key by single byte parts
    * Decipher file
    """
    file_buffer = bytearray()
    with open(in_file, 'r') as in_f:
        for line in in_f:
            file_buffer.extend(binascii.a2b_base64(line.strip()))

    keysize = get_keysize(file_buffer)

    blocks = [bytearray() for _ in xrange(keysize)]
    for num, char in enumerate(file_buffer):
        blocks[num % keysize].append(char)
    fullkey = bytearray()
    for num, block in enumerate(blocks):
        key_part = get_single_byte_xor_key(block)
        if key_part is None:
            raise ValueError("Can't brake some single byte xor part")
        fullkey.append(key_part)

    decipher_repeating_xor_file(fullkey, in_file)


#########
# TESTS #
#########
def test_hamming_distance():
    block1 = bytearray('this is a test')
    block2 = bytearray('wokka wokka!!!')
    return hamming_distance(block1, block2) == 37


def test_decipher_file():
    return break_repeating_xor('6.txt') is None


if __name__ == "__main__":
    for name, obj in globals().items():
        if name.startswith('test_'):
            print ('\033[1;32m.\033[1;m' if obj() else '\033[1;31mX\033[1;m'),
