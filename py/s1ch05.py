#!/usr/bin/python
import binascii


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


def repeating_xor_encipher(text, key):
    """
    Encipher text
    text - string of text to encipher
    key - key string
    returns - enciphered hex string
    """
    text = bytearray(text)
    key = bytearray(key)
    return binascii.hexlify(_repeating_xor(text, key))


def repeating_xor_decipher(text, key):
    """
    Decipher text
    text - deciphered string represented as hex
    key - key string
    returns - deciphered text string
    """
    text = bytearray.fromhex(text)
    key = bytearray(key)
    return _repeating_xor(text, key)


def encipher_file(in_file, out_file):
    """
    Encipher line by line in_file and write line by line to out_file
    """
    with open(in_file, 'r') as in_f, open(out_file, 'w') as out_f:
        for line in in_f:
            out_f.write(repeating_xor_encipher(line, 'ICE') + '\n')


def decipher_file(in_file, out_file):
    """
    Decipher line by line in_file
    Write to out_file without additional newlines
    """
    with open(in_file, 'r') as in_f, open(out_file, 'w') as out_f:
        for line in in_f:
            out_f.write(repeating_xor_decipher(line.strip(), 'ICE'))


#########
# TESTS #
#########
def test_repeating_xor_encipher():
    result = repeating_xor_encipher(
        "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal",
        "ICE"
    )
    expected = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    return result == expected


def test_repeating_xor_decipher():
    result = repeating_xor_decipher(
        "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f",
        'ICE'
    )
    expected = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    return result == expected


def test_encipher_file():
    encipher_file('test_file.txt', 'test_enc')
    return True


def test_decipher_file():
    decipher_file('test_enc', 'test_file2.txt')
    return True

if __name__ == "__main__":
    for name, obj in globals().items():
        if name.startswith('test_'):
            print ('\033[1;32m.\033[1;m' if obj() else '\033[1;31mX\033[1;m'),
