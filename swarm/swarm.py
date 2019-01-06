from multiprocessing import Pipe, Process
from .node_v import run_node


class Swarm():

    def __init__(s, local_nodes):
        s.pipes = {}
        s.processes = []

        for nodes_list in local_nodes:
            for node_name in nodes_list['names']:
                s.spawn(node_name, nodes_list['function'])        


    def spawn(s, name, function):
        """
        Create a new node(s) and add them to Swarm
        Parameters
        -------------
        func: a function to run on node(s)
        """
        pcnt = len(s.processes)

        if not pcnt :
            s.pipes[name] = {}
        else : 
            new_line = {}

            for line in s.pipes:
                own_end, anothers_end = Pipe()
                s.pipes[line][name] = anothers_end
                new_line[line] = own_end

            s.pipes[name] = new_line 


        p = Process(target=run_node, args=(name, function, s.pipes[name]))
        s.processes.append(p)

    def start(s):
        for p in s.processes:
            p.start()
