import multiprocessing as mps
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import time

def get_server(buff,pipe=None):

    class NodeServer(BaseHTTPRequestHandler):
        def _parse_params(s):
            qs = s.path.split('?')
            if len(qs)>1:
                return urllib.parse.parse_qs(qs[1])
            else:
                return {}

        def do_GET(s):

            print("got req")
            s.log_request()
            #req = s.parse_request()
            params = s._parse_params()
            print('params',params)
            #print(req)
            buff.append(params['foo'][0])
            if pipe:
                pipe.send(buff)

            s.send_response(200)
            s.wfile.write(bytes('OK\n'+str(buff),'utf-8'))

    return NodeServer

def start_server_parallel(addr):

    def serve(addr,pipe):
        buff = []
        ns =  get_server(buff,pipe)
        srv = HTTPServer(addr,ns)
        srv.serve_forever()

    a,b = mps.Pipe()
    p = mps.Process(target=serve, args=(addr,b))
    print('starting server')
    p.start()
    return a


if __name__=="__main__":
    pipe = start_server_parallel(('localhost',8083))

    while True:
        try:
            msg = pipe.recv()
        except Exception as e:
            msg = "<<noth>>"
            time.sleep(0.2)
            pass
        print("msg from srv",msg)

    b = ['1']
    ns =  get_server(b)

    srv = HTTPServer(('localhost',8083),ns)
    srv.serve_forever()
    print('aa')



class Node():

    def __init__(s, nodes_list, type_str='process'):
        """
        nodes is a list of dictionaries with type and adresses
        the first node is address for self

        """
        this_node_info = nodes_list[0]
        s.recv_buffer  = []

        if type_str=='process':
            s.addr = this_node_info['process_addr']
            s.pipe_in = this_node_info['pipe_in']
            s.intents = this_node_info['intents']
            s.type = type_str

        elif type_str=='network':
            pass
        else:
            raise Exception("Unrecognized node type:"+type_str)
        for nodeInfo in nodes_list[1:]:

            res = s._connect(nodeInfo)
            print('connection res:',res)

    def send(s,dest,msg):
        s.intents[dest] = addr
        pipe = s.pipes.get(dest)
        print('>>>sending to ',dest)
        pipe.send(msg)

    def recv(s):
        while True:
            intent = s.intents[s.addr]
            if intent!=-1:
                break
        pipe = s.pipes[intent]
        print('<<<getting from',intent)
        msg = pipe.recv()
        print(",,. got msg",msg)
        return msg

    def connect(s,info):
        pipe = info['pipe']


class Address():
    def __init__(s,addr,typ):
        s.addr = addr
        s.type = typ

class PipeEnd():
    def __init__(s,addr):
        s.addr = addr
        pass
    def send(s, addr, msg):
        pass
    def recv(s):
        return  0

class Pipe:
    def __init__(s, a,b, type_str='process'):
        """
        a and b are Addresses
        """
        if a.type!=b.type:
            raise Exception("types of addresses for pipe are:"+
                    a.type+","+b.type)
        if a.type == 'process':
            a_end,b_end = mps.Pipe()
            return a_end,b_end

        elif a.type == 'network':
            print("not supported network yet")










