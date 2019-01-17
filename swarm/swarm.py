from multiprocessing import Pipe, Process
from .node import run_node
from time import sleep


class Swarm():


    def __init__(self, local_nodes):

        self.MODE_FUNCTIONS = {
            'terminate' : self.mode_terminate, 
             'restart' : self.mode_restart 
        }

        self.pipes = {}
        self.processes = []

        for nodes_list in local_nodes:
            for node_name in nodes_list['names']:
                self.spawn(node_name, nodes_list['function'])      

        self.local_nodes = local_nodes


    def spawn(self, name, function):
        """
        Create a new node(s) and add them to Swarm
        Parameters
        -------------
        func: a function to run on node(s)
        """
        pcnt = len(self.processes)

        if not pcnt :
            self.pipes[name] = {}
        else : 
            new_line = {}

            for line in self.pipes:
                own_end, anothers_end = Pipe()
                self.pipes[line][name] = anothers_end
                new_line[line] = own_end

            self.pipes[name] = new_line 


        process = Process(name=name, target=run_node, daemon=True,
            args=(name, function, self.pipes[name], True))
        self.processes.append(process)


    def start(self):
        for process in self.processes:
            process.start()


    def monitor(self, mode):
        """
        Terminate mode : if one node falls then the entire network falls
        Restart mode : if some node falls swarm restarts it
        """
        if mode not in self.MODE_FUNCTIONS:
            print(mode, self.MODE_FUNCTIONS)
            raise NotImplementedError

        while True:
            exited_processes = [process for process in self.processes if 
                not process.is_alive()]

            if len(exited_processes) > 0:
                # Assumes 0 exit code is OK
                processes_exited_with_code = [process for process in exited_processes if 
                    process.exitcode > 0]
                for process in processes_exited_with_code:
                    if process.exitcode > 0:
                        print(f"Process {process.name} exited (exit code {process.exitcode})") # TODO implement traceback printing
                        process.close() # TODO close and delete pipes as well
                        self.processes.remove(process)
                        exited_processes.remove(process)

                interrupted_processes = [process for process in exited_processes if 
                    process.exitcode < 0]
                if len(interrupted_processes) > 0:
                    self.MODE_FUNCTIONS[mode](interrupted_processes)
            else:
                sleep(2) # TODO take this as optional from config


    def mode_terminate(self, interrupted_processes):
        print("\n")
        for process in interrupted_processes:
            print(f"Node {process.name} exited")
        print(f"Terminating all the other nodes")

        self.terminate_all_nodes()
        print("\nAll the nodes are terminated\n")

        raise SystemExit


    def terminate_all_nodes(self):
        for process in self.processes:
            if process.is_alive():
                process.kill()

        while True in [process.is_alive() for process in self.processes]:
            sleep(0.1)

        for process in self.processes:
            process.close()


    def mode_restart(self, interrupted_processes):
        print(f"\nEntering mode_restart. Processes: {interrupted_processes}")
        for process in interrupted_processes:
            print(f"Node {process.name} exited. Tring to restart it")

            for nodes_list in self.local_nodes:
                if process.name in nodes_list['names']:
                    name = process.name
                    process_index = self.processes.index(process)
                    self.processes[process_index] = Process(name=name, target=run_node, daemon=True, 
                        args=(name, nodes_list['function'], self.pipes[name], True))
                    process = self.processes[process_index]
                    sleep(3)
                    process.start()
                    sleep(2)
                    break # Against the case of double entry of this name in config

            if process.is_alive():
                print(f"Node {process.name} restarted : {process}")

        print("\tLeaving mode_restart")