#Piece of code responsible for constantly dealing with the
#BS UDP connections
import re
import socket
import sys
import argparse
import os
import shutil 

def getConnectionDetails():

	parser = argparse.ArgumentParser(description='Get connection details')
	parser.add_argument('-p', metavar='CSport', type=int, default=58011, help='Gives the port the user will connect to')

	connectionDetails = parser.parse_args()
	return connectionDetails.p

#General regex command matcher
def CMDMatcher(msg, pattern):
	matcher = re.compile(pattern)
	if matcher.match(msg):
		return 1
	return 0

#Simple function that sends the specified message through TCP
def sendTCPMessage(userSocket, msg):
	if not isinstance(msg, bytes):
		msg = msg.encode()
	userSocket.send(msg)

#Simple function that communicates in TCP
def communicateUDP(msg, BS_IP, BS_Port, BS_Socket):
	BS_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	BS_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	BS_Socket.sendto(msg.encode(),(BS_IP, int(BS_Port)))
	(msgRecv, BS_Server) = BS_Socket.recvfrom(1024)
	print(msgRecv)


#Cicle that keeps waiting for new BS's to register
def UDPConnections(CS_address,CS_port):
	BS_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	BS_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	BS_Socket.bind((CS_address, CS_port))	
	BS_Server = ''	
	msgRecv =''

	while True:
		(msgRecv, BS_Server) = BS_Socket.recvfrom(1024)
		print(BS_Server)
		msgRecv = msgRecv.decode().split(' ')
		print(msgRecv)
		RGR_msg = 'RGR '
		if CMDMatcher(msgRecv[0],'^REG$') and CMDMatcher(msgRecv[2],'^[0-9]{5}\n$'):
			file = open('backupServers.txt','ab+')
			file.write((msgRecv[1] + ' '+ msgRecv[2]).encode())
			file.close()
			RGR_msg+='OK\n'
		else:
			RGR_msg+='NOK\n'
		BS_Socket.sendto(RGR_msg.encode(),(BS_Server[0],int(BS_Server[1])))
	BS_Socket.close()
	return 0

#Function that eliminates the user from the list of users
def removeUser(username):
	os.remove('user_'+username+'.txt')
	shutil.rmtree('user_'+username,ignore_errors=True)
	return 1

#User authentication command
def AUTCommand(userSocket, message):
	autMsg = 'AUR '
	if CMDMatcher(message, '^AUT\s[0-9]{5}\s[0-9 a-z]{8}$'):
		message = message.split(' ')
		datafile = 'user_'+message[1] + '.txt'
		password = message[2].rstrip('\n')
		if os.path.exists(datafile):
			with open(datafile,'r') as file:
				if file.readline().rstrip('\n') == password.rstrip('\n'):
					autMsg += 'OK\n'
				else:
					autMsg += 'NOK\n'
		else:
			with open(datafile,'w') as file:
				file.write(password)
			os.makedirs('user_'+message[1])
			file = open('user_'+message[1]+'/'+'BS_Register.txt','w') 
			file.close()	
			autMsg += 'NEW\n'
	else:
		autMsg = 'ERR\n'

	sendTCPMessage(userSocket, autMsg)

	if autMsg != 'ERR\n' and autMsg != 'NOK\n':
		return 1
	return 0