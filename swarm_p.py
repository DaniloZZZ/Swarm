
"""
Written by Danil Lykov on 27/12/2018

This is a module for creating a pool of processes that communicate
with each other.

The ultimate goal is to create a p2p network of processes with abstract
communication either within network or between threads on one processor.
"""

import time
from multiprocessing import Process, Pipe, Array


class Socket():
    def __init__(s,idx,pipes,intent):
        s.pipes = []
        s.intent = intent
        s.idx = idx

    def _get_pipe(s,addr):
        # temporary stub, return pipe to main
        return s.pipes[0]

        return s.pipes[addr]

    def send(s,addr,msg):
        # wait if someone is communicating
        while True:
            if s.intent[0] == -2:
                break
            else:
              #print("#waiting to send to",addr,'from',intent[0])
              time.sleep(0.01)
        # wait if someone is communicating
        # Say that you want to transmit
        s.intent[0] = idx
        s.intent[1] = addr
        pipe = s._get_pipe(addr)
        pipe.send(msg)

    def recv(s):
        while True:
            if s.intent[1] == s.idx:
                print("I've got mail! reading from",intent[0])
                msg = pipe.recv()
                s.intent[0]=-1
                s.intent[1]=-1
                print("read message",msg)
                return msg
        pipe = s._get_pipe(addr)

        msg = pipe.recv()
        print("sock:received message from",addr)
        return msg

class Node:
    """
    A wrapper class for node data to pass to user
    """
    def __init__(s, number, socket):
        s.proc_num = number
        s.socket = socket

    def send(s,addr,msg):
        s.socket.send(addr,msg)
    def recv(s):
        return s.socket.recv()

def node( idx, function, socket, ):
    """
    A function that wraps the user's function that to be
    executed in this node.
    Parameters
    ---------
    idx: int
        index of the process, ie it's address
    function: a function to run
    pipe: a interface for communication
    """

    node = Node(idx, socket)
    print("starting function",idx)
    ret = function(node)
    print('node %d exited' % idx)
    return ret


class Swarm():
    def __init__(s,ports_range=None):
        s.nodes = []
        s.pipes = []
        s.processes = []
        s.intent = Array('i',range(2))

    def spawn(s,func, count=1):
        """
        Create a new node(s) and add them to Swarm
        Parameters
        -------------
        func: a function to run on node(s)
        """
        pcnt = len(s.processes)

        for i in range(count):
            one, another = Pipe()
            s.pipes.append((one,another))
            sock = Socket(pcnt+i, [another], s.intent)

            p = Process(target=node, args=(pcnt+i, func, sock))

            s.processes.append(p)
    def start(s ):
        for p in s.processes:
            p.start()
        while True:
            f = s.intent[0]
            if f >-1:
                to = s.intent[1]
                print(">>intent discovered by main",f,to)
                from_pipe = s.pipes[f][0]
                to_pipe = s.pipes[to][0]

                msg = from_pipe.recv()
                print ('>>main passes msg from to', f, to)
                to_pipe.send(msg)
                print(">>main sent msg from to",f,to)
                while s.intent[0]!=-1:
                  continue
                s.intent[0]=-2
                print(">>main: transition finished",f,to)
                #s.intent[0]=-1
                #s.intent[1]=-1

