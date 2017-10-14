
import math
import doctest

def w_binary_to_hex(word):
    """Converts binary word to hex (word is a list)

    >>> w_binary_to_hex("111")
    '0x7'

    >>> w_binary_to_hex([1,1,1,1])
    '0xf'

    >>> w_binary_to_hex([0,0,0,0,1,1,1,1])
    '0xf'

    >>> w_binary_to_hex([0,1,1,1,1,1,0,0])
    '0x7c'
    """

    if isinstance(word, str):
        return hex(int(word, 2))
    elif isinstance(word, list):
        bin_str = "".join(str(e) for e in word)
        return hex(int(bin_str, 2))

def sequence_to_words(s, bits_per_word=8):
    """Splits a sequence into its words

    >>> sequence_to_words([1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
    [[1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]]

    >>> sequence_to_words([1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], bits_per_word=4)
    [[1, 1, 1, 1], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]
    """
    
    return [s[bits_per_word*i:bits_per_word*i+bits_per_word] for i in range(0,math.ceil(len(s)/bits_per_word))]

def binary_seq_to_hex_words(bit_seq, bits_per_word=8, offset=0, endian='big'):
    """Converts a binary sequence (str) to its hex values

    Args:
        - bit_seq (str): The bit seqeunce
        - bits_per_word (int, optional): The number of bits per word
        - offset (int, optionnal): The number of bits to read from the sequence 
                                  first before splitting to words
        - endian (str, optional): either 'big' or 'little'

    >>> binary_seq_to_hex_words("101011111100010101101010")
    ['0xaf', '0xc5', '0x6a']

    >>> binary_seq_to_hex_words("111101011111100010101101010", offset=3)
    ['0x7', '0xaf', '0xc5', '0x6a']

    >>> binary_seq_to_hex_words("1101011111100010101101010", offset=1)
    ['0x1', '0xaf', '0xc5', '0x6a']

    >>> binary_seq_to_hex_words("101011111100010101101010", endian="little")
    ['0x56', '0xa3', '0xf5']
    """

    if endian == 'little':
        bit_seq = bit_seq[::-1]
    
    ret = []

    if offset != 0:
        offset_word = bit_seq[0:offset]
        bit_seq = bit_seq[offset::]
        ret.append(w_binary_to_hex(offset_word))

    words = sequence_to_words(bit_seq, bits_per_word=bits_per_word)
    for w in words:
        ret.append(w_binary_to_hex(w))

    return ret


def test():
    doctest.testmod()

if __name__ == '__main__':
    test()