HIDDEN_MAPPING = {
    # Unicode Character 'WORD JOINER' (U+2060) 0xE2 0x81 0xA0
    ' ': '\xE2\x81\xA0',
    # Unicode Character 'ZERO WIDTH SPACE' (U+200B) 0xE2 0x80 0x8B
    '0': '\xE2\x80\x8B',
    # Unicode Character 'ZERO WIDTH NON-JOINER' (U+200C) 0xE2 0x80 0x8C
    '1': '\xE2\x80\x8C',
}


def wrap(string: str) -> str:
    """Wrap a string with a distinct boundary."""
    # Unicode Character 'ZERO WIDTH NON-BREAKING SPACE' (U+FEFF) 0xEF 0xBB 0xBF
    return f'\xEF\xBB\xBF{string}\xEF\xBB\xBF'


def unwrap(string: str) -> str:
    """Unwrap a string if the distinct boundary exists."""
    temp = string.split('\xEF\xBB\xBF')

    if len(temp) == 1:
        return False
    return temp[1]


def str2bin(text: str) -> str:
    """Convert a string into binary data."""
    return ' '.join(format(i, 'b') for i in bytearray(text, 'utf-8'))


def bin2str(binary: str) -> str:
    """Convert binary data into a string."""
    return ''.join(str(int(i, 2)) for i in binary.split())


def bin2hidden(string: str) -> str:
    """Convert the ones, zeros, and spaces of the hidden binary data to their respective zero-width characters."""
    for char, zero_width in HIDDEN_MAPPING.items():
        string = string.replace(char, zero_width)
    return string


def hidden2bin(string: str) -> str:
    """Convert zero-width characters to hidden binary data."""
    for char, zero_width in HIDDEN_MAPPING.items():
        string = string.replace(zero_width, char)
    return string


def encode(public: str, private: str) -> str:
    """Hide a private message within a public message."""
    half = round(len(public) / 2)

    private_bin = str2bin(private)
    private_zero_width = bin2hidden(private_bin)
    private_wrapped = wrap(private_zero_width)

    public_steganographised = ''.join([public[:half], private_wrapped, public[half:]])
    return public_steganographised


def decode(public: str) -> str:
    """Reveal the private message hidden within a public message."""
    unwrapped = unwrap(public)

    if not unwrapped:
        message = bin2str(hidden2bin(public))
    else:
        message = bin2str(hidden2bin(unwrapped))

    # If encoded ampersands are present, convert them to regular ampersands.
    message = message.replace('&amp;', '&')

    if len(message) < 2:
        message = 'Notice: No private message was found.'

    return message


if __name__ == '__main__':
    # informal tests
    wrapped = wrap('test')
    print(wrapped)
    print(wrapped.split('\xEF\xBB\xBF'))
    print(unwrap(wrapped))

    encoded = encode('hello world', 'never gonna give you up')
    print(encoded)
    print(decode(encoded))
