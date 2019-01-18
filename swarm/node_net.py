
from sys import argv
import time
import socketserver
from multiprocessing.dummy import Process as Thread, Pipe
from network.piped_server import PipedThreadedServer
import network.net_utils as utils
import network.protocol as protocol

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
                """
                Starts the network server to listen for messages
                initiates connection with every node.
                after every node from config connected starts
                user function
                """

                s._print("starting...")
                s._start_threads()
                s._handshake(s.network)
                s._print("Connection with network established!")
                s._print("##calling user fucntion")
                ret = s.func(s)
                s._print('user func returned',ret)
                return ret

        def send(s, to, data):
                node = s._get_node_by_name(to)
                msg = protocol.form_data_message(data)
                utils.send_to(msg, (node['host'], node['port']) )

        def recv(s,sender=None):
            msg_bytes = s.server_pipe.recv(sender = sender)
            #TODO: do not receive all data if mailformed message
            # now we send oly strings
            return protocol.get_message_data(msg_bytes)

        def _handshake(s, network):
            """
            Sends a connect signal to every node in network
            then listens for response from every node in network
            """
            msg = protocol.form_connect_message(s.name)
            network = [n for n in network if n['name']!=s.name]
            names = [n['name'] for n in  network ]

            for node in network:
                while True:
                    try:
                        utils.send_to(msg, (node['host'],node['port']) )
                        break
                    except ConnectionRefusedError as e:
                        #s._print('conn refused')
                        time.sleep(0.01)

            while len(names):
                msg = s.server_pipe.recv()
                msg_type = protocol.get_message_type(msg)

                if msg_type==protocol.MessageType.CONNECT:
                    name = protocol.get_message_data(msg)
                    s._print('got connection from',name)
                    names.remove(name)
                else:
                    s._print("warning: got unwanted message")


        def _start_threads(s):
                s.server_pipe, pipe_end = Pipe(duplex=False)
                s.server = PipedThreadedServer(s.port, pipe_end)


        def _print(s,*args):
                print("<<node %s:"%s.name,*args)

        def _get_node_by_name(s,name):
                r = [n for n in s.network if n['name']==name]
                assert len(r)==1, 'Wrong network info in node'+s.name
                return r[0]
