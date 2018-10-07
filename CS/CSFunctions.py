#Piece of code responsible for constantly dealing with the
#BS UDP connections
import re
import socket
import sys
import argparse

def getConnectionDetails():

	parser = argparse.ArgumentParser(description='Get connection details')
	parser.add_argument('-p', metavar='CSport', type=int, default=58032, help='Gives the port the user will connect to')

	connectionDetails = parser.parse_args()
	print(connectionDetails.p)
	return connectionDetails.p

def UDPConnections(CSport):

	BS_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	BS_Server = ''
	msgRecv =''

	while 1:
		(msgRecv, BS_Server) = CS_Socket.recvfrom(1024)
		msgRecv.split(' ')
		#FIX ME: DEFINE THE REST OF THE PROTOCOL

	file = open('backupServers.txt','w')
	file.write('Tejo e fixe\n')
	file.close()

#General regex command matcher
def CMDMatcher(msg, pattern):
	matcher = re.compile(pattern)
	if matcher.match(msg):
		return 1
	return 0


#Checks if the user exists
def checkUser(username,password):

	file = open('utilizadores.txt','r')

	for line in file.readlines():
		temporary = line.split(' ')

		if username == temporary[0]:
			if password != temporary[1].rstrip('\n'):
				file.close()
				return 'NOK'
			file.close()
			return 'OK'

	file.close()
	file = open('utilizadores.txt','ab+')	
	package = username + ' ' + password + '\n'
	file.write(package.encode())
	file.close()
	return 'NEW'

#User authentication command
def AUTCommand(message):
	if CMDMatcher(message, '^AUT\s[0-9]{5}\s[0-9 a-z]{8}$'):
		return 1
	return 0


def DLUCommand(username,password):
	return 0

def BCKCommand(msgRecv):
	return 0

def RSTCommand(msgRecv):
	return 0

def LSDCommand(username,password):
	return 0

def LSFCommand(msgRecv):
	return 0

def DELCommand(msgRecv):
	return 0