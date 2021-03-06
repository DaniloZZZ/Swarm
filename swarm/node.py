from multiprocessing.connection import wait


class Node:
    """
    A wrapper class for node data to pass to user
    """
    def __init__(s, name, pipes):
        s.name = name
        s.pipes = pipes

    def send(s, addr, msg):
        s.pipes[addr].send(msg)

    def recv(s, addr=None):
        if addr:
            return s.pipes[addr].recv()
        else:
            for waiter in wait(s.pipes):
                msg = waiter.recv()
                return msg


def run_node(name, function, pipes, verbose=False):
    """
    A function that wraps the user's function that is to be
    executed in this node.
    Parameters
    ---------
    idx: int
        index of the process, ie it's address
    function: a function to run
    pipe: a interface for communication
    """

    if verbose: import os
    node = Node(name, pipes)
    if verbose: print("Node {} started, pid {}".format(name, os.getpid()))
    ret = function(node)
    if verbose: print("Node %s exited" % name)
    return ret
