import socket
import sys
import argparse

def getConnectionDetails():

	parser = argparse.ArgumentParser(description='Get connection details to connect to server.')
	parser.add_argument('-n', metavar='CSname', type=str, default='localhost', help='gives the name of the address do connect')
	parser.add_argument('-p', metavar='CSport', type=int, default=58032, help='gives the port the user will connect to')

	connectionDetails = parser.parse_args()
	
	return (connectionDetails.n, connectionDetails.p)
	
def recvMessage(mySocket, size, msgSent):
	
	mySocket.send(msgSent.encode())

	msgRecv = ''.encode()
	
	while (msgRecv[-1:].decode() != "\n"):
		msgRecv = msgRecv.decode() + (mySocket.recv(size)).decode()
		msgRecv = msgRecv.encode()
	
	msgRecv = msgRecv.decode()

	return msgRecv

def LSDCommand(mySocket, size):
	
	msgSent = "LSD\n"
	
	msgRecv = recvMessage(mySocket, size, msgSent)

	if msgRecv[0: len('LDR ')] == 'LDR ':
		print(msgRecv[4:], end='')

	return 1

#The command that processes the Delete user request
def DLUCommand(mySocket, size):
		
		msgSent = 'DLU\n'
		
		msgRecv = recvMessage(mySocket, size, msgSent)

		if msgRecv[0: len("DLR ")] == "DLR ":
			print(msgRecv[len("DLR "):], end="")
			if msgRecv[len("DLR "):] == "OK":
				print(msgRecv[len("DLR "):])
				return 0;
		return 1;