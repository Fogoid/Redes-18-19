import socket
import sys
import argparse
import re
import os


def getConnectionDetails():

	parser = argparse.ArgumentParser(description='Get connection details to connect to server.')
	parser.add_argument('-n', metavar='CSname', type=str, default='localhost', help='Gives the name of the address do connect')
	parser.add_argument('-p', metavar='CSport', type=int, default=58032, help='Gives the port the user will connect to')

	connectionDetails = parser.parse_args()
	return (connectionDetails.n, connectionDetails.p)
	
def CMDMatcher(msg, pattern):
	matcher = re.compile(pattern)
	if matcher.match(msg):
		return 1
	return 0

def sendMessage(mySocket, msgSent):
	mySocket.send(msgSent.encode())

def recvMessage(mySocket):
	msg = ''.encode()
	
	while True:
		data = mySocket.recv(8)
		if not data:
			break
		msg += data
	
	print((msg, "this was a received message"))
	return msg

def recvFixedMessage(mySocket):
	msg = mySocket.recv(128).decode()
	print((msg, "this was a received message"))
	return msg
