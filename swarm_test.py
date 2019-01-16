from swarm.swarm import Swarm

if __name__=="__main__":

    def master_func(node):
        print("i am process", node.name)
        received_in_total = 0
        for slave in ['slave%d' % i for i in range(1, 4)]:
            print("listening")
            r = node.recv()
            print("###>>Me, the %s got " % node.name, r)
            received_in_total += 1
            print("###>>total got:", received_in_total)
    
    def slave_func(node):
        print("i am process", node.name)
        print("###<<sending from %s to master" % node.name)
        s = node.send('master', "hello from %s" % node.name)


    swr = Swarm(mode='strict', local_nodes=[
        {
            'names' : ['master'], 
            'function' : master_func,
        }, {
            'names' : ['slave%d' % i for i in range(1, 4)], 
            'function' : slave_func,
        }
    ])
    swr.start()
