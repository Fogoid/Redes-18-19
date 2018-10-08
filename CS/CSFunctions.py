#Piece of code responsible for constantly dealing with the
#BS UDP connections
import re
import socket
import sys
import argparse
import os
from shutil import rmtree

def getConnectionDetails():

	parser = argparse.ArgumentParser(description='Get connection details')
	parser.add_argument('-p', metavar='CSport', type=int, default=58011, help='Gives the port the user will connect to')

	connectionDetails = parser.parse_args()
	print(connectionDetails.p)
	return connectionDetails.p

#General regex command matcher
def CMDMatcher(msg, pattern):
	matcher = re.compile(pattern)
	if matcher.match(msg):
		return 1
	return 0

#Simple function that sends the specified message through TCP
def sendTCPMessage(msg,User_Socket):
	User_Socket.send(msg.encode())

#Cicle that keeps waiting for new BS's to register
def UDPConnections(CSport):

	BS_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	BS_Server = ''
	msgRecv =''

	while 1:
		(msgRecv, BS_Server) = BS_Socket.recvfrom(1024).decode()
		msgRecv.split(' ')
		RGR_msg = ''
		if CMDMatcher(msgRecv[0],'^REG$') and CMDMatcher(msgRecv[2],'^[0-9]{5}\n$'):
			file = open('backupServers.txt','ab+')
			file.write((msgRecv[1] + msgRecv[2].rstrip('\n')).encode())
			file.close()
			Bs_Socket.sendto('OK\n'.encode(),(msgRecv[1],msgRecv[2].rstrip('\n')))
		else:
			BS_Socket.sendto('RGR ERR\n'.encode(),(msgRecv[1],msgRecv[2].rstrip('\n')))
	return 0



#Function that eliminates the user from the list of users
def removeUser(username):
	os.remove("user_"+username+'.txt')
	shutil.rmtree(username,ignore_errors=True)
	return 1

#User authentication command
def AUTCommand(message,User_Socket):
	AUT_msg = ''
	if CMDMatcher(message, '^AUT\s[0-9]{5}\s[0-9 a-z]{8}$'):
		message = message.split(' ')
		datafile = 'user_'+message[1] + '.txt'
		password = message[2].rstrip('\n')
		if os.path.exists(datafile):
			with open(datafile,'r') as file:
				if file.readline().rstrip('\n') == password.rstrip('\n'):
					AUT_msg = 'OK\n'
				else:
					AUT_msg = 'NOK\n'
		else:
			with open(datafile,'w') as file:
				file.write(password)
			os.makedirs('user_'+message[1])	
			AUT_msg = 'NEW\n'
	else:
		AUT_msg = 'ERR\n'

	sendTCPMessage(AUT_msg,User_Socket)

	if AUT_msg != 'ERR\n' and AUT_msg != 'NOK\n':
		return 1
	return 0


def DLUCommand(serverSocket,username):
	DLR_msg = 'DLR '

	filename = username+'.txt'
	if os.path.exists(filename):
		if os.stat(filename).st_size == 0:
			os.remove(filename)
			removeUser(username)
			DLR_msg +='OK\n'
	else:
		DLR_msg +='NOK\n'

	sendTCPMessage(DLR_msg,serverSocket)
	return 0

def BCKCommand(msgRecv):
	return 0

def RSTCommand(msgRecv,username,User_Socket):

	RSR_msg ='RSR '
	if CMDMatcher(msgRecv, '^RST\s[a-z]+\n$'):
		msgRecv=msgRecv.split(' ')
		if os.path.exists('user_'+username+'/'+msgRecv[1]):
			with open('user_'+username+'/'+msgRecv[1]+'/'+'IP_port.txt','r') as file:
				 RSR_msg += file.readline()+'\n'
		else:
			RSR_msg += 'EOF\n'
	else:
		RSR_msg='ERR\n'

	sendTCPMessage(User_Socket,RSR_msg)
	return 0

def LSDCommand(username,User_Socket):

	LDR_msg ='LDR '
	dirnameList = ''
	username_directory = "user_"+username
	n = 0

	if os.path.exists(username_directory):
		for dirpath, dirnames, files in os.walk("./" + username_directory):
			for name in dirnames:
				n += 1
				dirnameList += name+' '

	LDR_msg += str(n) + ' ' + dirnameList + '\n'
	sendTCPMessage(LDR_msg,User_Socket)
	return 0

def LSFCommand(msgRecv,username,User_Socket):
	LFD_msg='LFD '
	username_directory = "user_"+username


	if CMDMatcher(msgRecv, '^LSF\s[a-z]+\n$'):
		msgRecv=msgRecv.split(' ')
		msgRecv[1] = msgRecv[1].rstrip('\n')
		if os.path.exists(username_directory+'/'+msgRecv[1]):
			with open(username_directory+'/'+msgRecv[1]+'/'+'IP_port.txt','r') as file:
				bs_data = file.readline().split(' ')
				BS_Server.append(bs_data[0])
				BS_Server.append(bs_data[1])
			LFD_msg += BS_Server[0]+' '
			LFD_msg += BS_Server[1]+' '
	else:
		LFD_msg='ERR\n'

	sendTCPMessage(User_Socket,LFD_msg)
	return 0

def DELCommand(msgRecv,username,User_Socket):
	DDR_msg = 'DDR '
	username_directory = "user_"+username
	BS_Server = []


	if CMDMatcher(msgRecv, '^DEL\s[a-z]+\n$'):
		msgRecv=msgRecv.split(' ')
		msgRecv[1] = msgRecv[1].rstrip('\n')
		if os.path.exists(username_directory+'/'+msgRecv[1]):
			with open(username_directory+'/'+msgRecv[1]+'/'+'IP_port.txt','r') as file:
				bs_data = file.readline().split(' ')
				BS_Server.append(bs_data[0])
				BS_Server.append(bs_data[1])
			#FIX ME : SEND BS SERVER INSTRUCTION TO DESTROY DIR
			shutil.rmtree(username_directory+'/'+msgRecv[1],ignore_errors=True)
			DDR_msg += 'OK\n'
		else:
			DDR_msg += 'NOK\n'
	else:
		DDR_msg='ERR\n'
	sendTCPMessage(User_Socket,DDR_msg)
	return 0