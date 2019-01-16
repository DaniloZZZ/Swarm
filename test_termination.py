from service.swarm import Swarm
from server import main as server_func


def everlong_fn(node):
    while True:
        pass

def dummy_fn(node):
    return

def main():
    swr = Swarm(local_nodes=[
        {
            'names' : ['server'], 
            'function' : everlong_fn,
        },
        {
            'names' : ['everlong'], 
            'function' : everlong_fn,
        },
        {
            'names' : ['everlong2'], 
            'function' : everlong_fn,
        },
        {
            'names' : ['everlong3'], 
            'function' : dummy_fn,
        },

    ])
    
    import os
    print("Main process pid %d" % os.getpid())
    swr.start()
    swr.monitor('terminate')

if __name__=="__main__":
    main()
