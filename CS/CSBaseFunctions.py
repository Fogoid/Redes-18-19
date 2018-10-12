#Piece of code responsible for constantly dealing with the
#BS UDP connections
import re
import socket
import sys
import argparse
import os
import shutil


#Try catches for initializing a TCP socket
def TCPSocket():
		try:
			TCP_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			TCP_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		except socket.error as e:
			print ('Error creating TCPSocket\nTerminating Process')
			sys.exit(1)
		return TCP_Socket

#Try catches for initializing a UDP socket
def UDPSocket():
	try:
		UDP_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		UDP_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	except socket.error as e:
		print ('Error creating socket: UDPSocket\nTerminating Process')
		sys.exit(1)
	return UDP_Socket

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
	try:
		if not isinstance(msg, bytes):
			msg = msg.encode()
		userSocket.send(msg)
	except socket.error as e:
		print ('Error sending message from TCPSocket to User\nTerminating Process')
		sys.exit(1)
	return 0


#Simple function that communicates in TCP
def communicateUDP(msg, BS_IP, BS_Port):
	try:
		BS_Socket = UDPSocket()
		BS_Socket.sendto(msg.encode(),(BS_IP, int(BS_Port)))
	except socket.error as e:
		print ('Error sending message from UDPSocket to BS\nTerminating Process')
		sys.exit(1)
		
	data = ''
	UDPmsg = ''
	try:
		(UDPmsg,BS_address) = BS_Socket.recvfrom(1024)
		UDPmsg = UDPmsg.decode()
	except socket.error as e:
		print ('Error receiving message from UDPSocket sent by BS\nTerminating Process')
		sys.exit(1)
	BS_Socket.close()
	return UDPmsg

#Cicle that keeps waiting for new BS's to register
def UDPConnections(CS_address,CS_port):

	while True:
		BS_Socket = UDPSocket()
		BS_Socket.bind((CS_address, CS_port))

		BS_Server = ''
		msgRecv = b''

		while not msgRecv != b'':
			(msgRecv, BS_Server) = BS_Socket.recvfrom(1024)

		msgRecv = msgRecv.decode()
		splitedMsg = msgRecv.split(' ')

		msg = ''
		if CMDMatcher(splitedMsg[0], '^UNR$'):
			msg += 'UAR '
			if CMDMatcher(msgRecv, '^UNR\s[0-9 .]+\s[0-9]{5}\n$'):

				print('BS '+'UNR '+splitedMsg[1] + ' ' + splitedMsg[2].rstrip('\n'))
				msg += 'OK\n'
			else:
				msg += 'ERR\n'

		elif CMDMatcher(splitedMsg[0],'^REG$'):
			msg += 'RGR '
			if CMDMatcher(msgRecv,'^REG\s[0-9 .]+\s[0-9]{5}\n$'):
			
				try:
					file = open('backupServers.txt','ab+')
					print('BS '+'RGR '+splitedMsg[1] + ' ' + splitedMsg[2].rstrip('\n'))
					file.write((splitedMsg[1] + ' '+ splitedMsg[2]).encode())
					file.close()
				except (OSError, IOError) as e:
					print('Error writing in the file: backupServers.txt \n')
				msg+='OK\n'
			else:
				msg += 'ERR\n'
		else:
			msg ='ERR\n'

		BS_Socket.sendto(msg.encode(),(BS_Server[0],int(BS_Server[1])))

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
	if CMDMatcher(message, '^AUT\s[0-9]{5}\s[0-9 A-Z a-z]{8}$'):
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
			try:
				with open(datafile,'w') as file:
					file.write(password)
				os.makedirs('user_'+message[1])
				file = open('user_'+message[1]+'/'+'BS_Register.txt','w')
				file.close()
				autMsg += 'NEW\n'
			except (OSError, IOError) as e: 				
				print('Error writing in the file: BS_Register.txt \n')
	else:
		autMsg = 'ERR\n'

	sendTCPMessage(userSocket, autMsg)

	if autMsg != 'ERR\n' and autMsg != 'NOK\n':
		return 1
	return 0
