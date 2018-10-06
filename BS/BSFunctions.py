import socket
import sys
import argparse
import re

def getConnectionDetails():

	parser = argparse.ArgumentParser(description='Get connection details to connect to server.')
	parser.add_argument('-b', metavar='BSport', type=int, default=59000, help='Well-know available port for the CS and user to connect to')
	parser.add_argument('-n', metavar='CSname', type=str, default='localhost', help='Name of the CS where the BS will connect to')
	parser.add_argument('-p', metavar='CSport', type=int, default=58032, help='Port from CS where the BS will connect to')

	connectionDetails = parser.parse_args()
	print((connectionDetails.n,connectionDetails.p))
	return (connectionDetails.n, connectionDetails.p)

#General regex command matcher
def CMDMatcher(msg, pattern):
	matcher = re.compile(pattern)
	if matcher.match(msg):
		return 1
	return 0

def SendError(CS_Socket,address,port):
	error_msg = 'ERR'
	CS_Socket.sendto(error_msg.encode(),(address,port))


def startBS(CS_Socket,address,port):

	register = 'REG '+address+' '+str(port)+'\n'
	msgRecv = ""
	centralServer = ''

	while 1:
		CS_Socket.sendto(register.encode(),(address,port))
		(msgRecv, centralServer) = CS_Socket.recvfrom(1024)
		msgRecv = msgRecv.decode()
		print(msgRecv)

		if msgRecv == "RGR OK\n":
			return 1
	return 0

def LSFCommand():
	return 0

def LSUCommand():
	return 0

def DLBCommand():
	return 0