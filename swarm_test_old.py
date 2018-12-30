"""
Written by Danil Lykov on 27/12/2018

This is a module for creating a pool of processes that communicate
with each other.

The ultimate goal is to create a p2p network of processes with abstract
communication either within network or between threads on one processor.
"""

import time
from multiprocessing import Process, Pipe, Array

class PipeEnd():
    def __init__(s,src,dest):
        s.src = dest
        s.dest =  dest

    def send(s,message):
        print("Network communication isnt implemented yet")
        return 0
    def recv():
        message = 0
        return message

def PipeNetwork(ports):
    one = PipeEnd(ports[0],ports[1])
    other = PipeEnd(ports[1],ports[0])

def PipeProcess():
    return Pipe()

class Node:
    """
    A wrapper class for node data to pass to user
    """
    def __init__(s, number, send, recv ):
        s.proc_num = number
        s.send = send
        s.recv = recv

def node( idx, function, intent, pipe, ):
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

    def send(addr, msg):
        # wait if someone is communicating
        while True:
            if intent[0] == -2:
                break
            else:
              #print("#waiting to send to",addr,'from',intent[0])
              time.sleep(0.01)
        # Say that you want to transmit
        intent[0] = idx
        intent[1] = addr
        print("INtent set by",idx,intent[0],intent[1])
        pipe.send(msg)

    def recv():
        while True:
            if intent[1] == idx:
                print("I've got mail! reading from",intent[0])
                msg = pipe.recv()
                intent[0]=-1
                intent[1]=-1
                print("read message",msg)
                return msg
    node = Node(idx, send, recv)
    print("starting function",idx)
    ret = function(node)
    print('node %d exited' % idx)
    return ret

class Swarm:
    def __init__(s, count=1):
        s.intent_array = Array('i', range(2))
        print ('making swarm of %d processes' % count)
        s.count = count

    def spawn(s, func):
        processes = []
        pipes = [ PipeProcess() for i in range(s.count)]
        s.intent_array[0]=-2
        s.intent_array[1]=-2
        for i in range(s.count):
            (parent, child) = pipes[i]
            p = Process(target=node, args=(i, func, s.intent_array,
                        child))

            processes.append(p)
        for p in processes:
          p.start()
        while True:
            f = s.intent_array[0]
            if f >-1:
                to = s.intent_array[1]
                print(">>intent discovered by main",f,to)
                from_pipe = pipes[f][0]
                to_pipe = pipes[to][0]

                msg = from_pipe.recv()
                print ('>>main passes msg from to', f, to)
                to_pipe.send(msg)
                print(">>main sent msg from to",f,to)
                while s.intent_array[0]!=-1:
                  continue
                s.intent_array[0]=-2
                print(">>main: transition finished",f,to)
                #s.intent_array[0]=-1
                #s.intent_array[1]=-1
if __name__=="__main__":
    #Basic usage:
    swarm = Swarm(10)
    def func(node):

        idx = node.proc_num
        print("i am process",idx)
        if idx!=2:
            print("###<<sending from %d  to 2"%idx)
            s = node.send(2,"hello from %i"%idx)
        else:
            a = 0
            while True:
                print("listnng")
                r = node.recv()
                print("###>>Me, the %d got "%idx,r)
                a+=1
                print("###>>total got:",a)

    swarm.spawn(func)
