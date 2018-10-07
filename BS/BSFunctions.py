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

def verifyUser(username,password):
	file = open('users.txt','r')

	for line in file.readlines():
		temporary = line.split(' ')

		if username == temporary[0]:
			if password != temporary[1].rstrip('\n'):
				file.close()
				return 'NOK'
			file.close()
			return 'OK'
	return 'NOK'

def LSFCommand(msgRecv,CS_Socket,address,port):
	return 0

#Responsible for handling the server LSU request, CS server
#requests a new user to be registered
def LSUCommand(msgRecv,CS_Socket,address,port):
	LUR_msg=''

	if CMDMatcher(msgRecv[0]+msgRecv[1]+msgRecv[2], '^AUT\s[0-9]{5}\s[0-9 a-z]{8}$'):
		file = open('users.txt','r')
		for line in file.readlines():
			temporary = line.split(' ')
			if username == temporary[0]:
				file.close()
				LUR_msg='LUR NOK\n'
				break

		if(LUR_msg!='LUR NOK\n'):
			file = open('users.txt','ab+')	
			package = username + ' ' + password + '\n'
			file.write(package.encode())
			file.close()
			LUR_msg ='LUR OK\n'

	else:
		LUR_msg ='LUR ERR\n'

	CS_Socket.sendto(LUR_msg.encode(),(address,port))
	return 0



def DLBCommand(msgRecv,CS_Socket,address,port):
	return 0