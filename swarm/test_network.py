from swarm_net import SwarmNetwork

config = [

        { 'name':'A',
            'host':'localhost', },
        { 'name':'B',
            'host':'localhost', },
        { 'name':'C',
            'host':'localhost', }
        ]

def _print(node,*arg):
    print("###%s got"%node.name,*arg)

def func(node):
    print("I am node",node.name,'with pid',node.pid)
    if node.name=='A':
        node.send('B','hello from a')
    elif node.name=='B':
        msg = node.recv()
        _print(node,'got',msg)
    else:
        print("i'm the C and waiting")
        msg = node.recv()


def main():
    sw = SwarmNetwork()
    for node in config:
        sw.spawn(node['name'], func, host=node['host'] )

    sw.start()


if __name__=='__main__':
    main()
