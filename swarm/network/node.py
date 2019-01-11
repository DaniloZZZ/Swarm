
from sys import argv
import socket
import socketserver
from multiprocessing.dummy import Process as Thread, Pipe

class Node:

        def __init__(s,
                func,
                name,
                host,
                pid,
                port,
                network ):

            s.func = func
            s.name = name
            s.host = host
            s.network = network
            s.pid = pid
            s.port = port

        def start(s):
            s._print("starting...")
            s._start_threads()

        def _start_threads(s):
            ret = s.func(s)
            s._print('user func returned',ret)
            return ret

        def _print(s,*args):
            print("<<node %s"%s.name,*args)

        def _get_node_by_name(s,name):
            r = [n for n in s.network if n['name']==name]
            assert len(r)==0, 'Wrong network info in node'+s.name
            return r[0]

        def _send_to_node(s, data, node):
            host = node['host']
            port = node['port']
            s._print('sending to'+host+':'+port)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, int(port) ))
                sock.sendall(bytes(data + "\n", "utf-8"))
                sock.shutdown(socket.SHUT_RDWR)

        def send(s, to, data):
            node = s._get_node_by_name(to)
            s._send_to_node(data, node)

        def recv(s):
            pass
