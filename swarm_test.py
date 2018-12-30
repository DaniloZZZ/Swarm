
from swarm import Swarm

if __name__=="__main__":
    swr = Swarm()
    def func(node):
        idx = node.proc_num
        print("i am process",idx)
        if idx!=2:
            print("###<<sending from %d  to 2"%idx)
            s = node.send(2,"hello from %i"%idx)
        else:
            a = 0
            while True:
                print("listnng")
                r = node.recv()
                print("###>>Me, the %d got "%idx,r)
                a+=1
                print("###>>total got:",a)

    [swr.spawn( func ) for i in range(6)]
    swr.start()
