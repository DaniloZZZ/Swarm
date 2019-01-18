from swarm_net import SwarmNetwork
import time

config = [

        { 'name':'A',
            'host':'localhost', },
        { 'name':'B',
            'host':'localhost', },
        { 'name':'C',
            'host':'localhost', }
        ]

def _print(node,*arg):
    print("###%s"%node.name,*arg)

def func(node):
    print("I am node",node.name,'with pid',node.pid)
    if node.name=='A':
        node.send('B','hello from a')
        for i in range(10):
            msg = node.recv()
            _print(node,i,'got',msg)
            time.sleep(0.03)
            node.send('B',msg+', a')

    elif node.name=='B':
        for i in range(10):
            msg = node.recv()
            _print(node,i,'got',msg)
            node.send('C',msg+',b')
    else:
        for i in range(10):
            msg = node.recv()
            _print(node,i,'got',msg)
            node.send('A',msg+',c')


def main():
    sw = SwarmNetwork()
    for node in config:
        sw.spawn(node['name'], func, host=node['host'] )

    sw.start()


if __name__=='__main__':
    main()
