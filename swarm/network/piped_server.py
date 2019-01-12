
from sys import argv
import socket
import socketserver
from multiprocessing.dummy import Process as Thread, Pipe

class PipedThreadedServer(Thread):
        """
        Sets the pipe that is used for sending the results of request handling
        to another process or thread because the server is run in a separate one
        """

        class TCPServer(socketserver.TCPServer):

                def __init__(self, pipe, *args, **kwargs):
                        self.pipe = pipe
                        super(PipedThreadedServer.TCPServer, self).__init__(*args, **kwargs)


        class RequestHandler(socketserver.BaseRequestHandler):

                def handle(self):
                        data = self.request.recv(1024).strip()
                        self.server.pipe.send( data )


        def __init__(self, server_port, pipe, **kwargs):
                super(PipedThreadedServer, self).__init__()
                self.server_port = server_port
                self.pipe = pipe
                self.daemon = True
                self.start()


        def run(self):
                with PipedThreadedServer.TCPServer(self.pipe, ("localhost", self.server_port),
                        PipedThreadedServer.RequestHandler) as server:
                        server.serve_forever()

