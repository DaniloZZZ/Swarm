
def int_to_bytes(i):
    # TODO: this should belong somewhere to "utils" file
    least = i%256
    big = i//256
    return bytes([big,least])
def bytes_to_int(b):
    # TODO: this should belong somewhere to "utils" file
    big = b[0]
    least = b[1]
    return int(256*big+least)
