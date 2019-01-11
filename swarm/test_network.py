from swarm_net import SwarmNetwork

config = [

        { 'name':'A',
            'host':'tis', },
        { 'name':'B',
            'host':'tis', },
        { 'name':'C',
            'host':'tis', }
        ]
def func(node):
    print("I am node",node.name,'with pid',node.pid)

def main():
    sw = SwarmNetwork()
    for node in config:
        sw.spawn(node['name'], func, host=node['host'] )

    sw.start()


if __name__=='__main__':
    main()
