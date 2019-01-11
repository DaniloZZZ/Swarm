from multiprocessing import Pipe, Process
from network.node import Node


class SwarmNetwork():

    def __init__(s):
        s.ports_iter = (i for i in range(9001,9099))

        s.nodes_list = []
        s.network = []
        s.functions = {}

    def set_config(s, config):
        s.config=config

    def spawn(s, name, function, host='localhost'):
        """
        Create a new node(s) and add them to Swarm
        Parameters
        -------------
        name: name of node
        func: a function to run on node(s)
        host: host of node
        """

        pid = len(s.network)
        port = next(s.ports_iter)
        node_info = {
                'name':name,
                'host':host,
                'pid':pid,
                'port':port,
                }
        s.network.append(node_info)
        s.functions[name] = function


    def start(s):
        print('init',s.network)
        for node_info in s.network:
            node = Node(
                    s.functions[node_info['name']],
                    network=s.network,
                    **node_info
                    )
            f = lambda node: node.start()

            p = Process(target=f, args=(node,),name=node.name+"#"+str(node.pid))
            print("starting %s"%node.name)
            p.start()

