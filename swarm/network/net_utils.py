import socket

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

def send_to(data, addr):
    host, port = addr
    #s._print('sending to'+host+':'+str(port))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, int(port) ))
        sock.sendall(data)
        sock.shutdown(socket.SHUT_RDWR)
