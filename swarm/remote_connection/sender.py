from node import Node
from sys import argv


def main():

	serving_port = int(argv[1])
	receiving_port = int(argv[2])
	
	node = Node(serving_port, receiving_port)
	node.send("I'm a sender")
	print("Sender received : " + node.recv())


if __name__ == "__main__":
	main()