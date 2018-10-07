import socket
import sys
import argparse
import re
import os
import time

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

def authenticateUser(mySocket):

	while True: 
		userLogin = input()
		
		if(CMDMatcher(userLogin,'^login\s[0-9]{5}\s[0-9 a-z]{8}$')):

			(cmd, username, password) = userLogin.split(' ')

			status = AUTCommand(mySocket, username, password)

			if status == 'OK\n':
				print("User login successful")
			elif status == 'NOK\n':
				print("Wrong password") 
				continue
			else:
				print("A new user was created with your credentials")

			return (username, password, 0)

		elif CMDMatcher(userLogin, '^exit$'):
			return ("NNNNN", "NNNNNNNN", 1, "none")
		else:
			print("Please insert login XXXXX NNNNNNNN\nXXXXX - Your login 5 digit number\nNNNNNNNN - Your 8 character long password")

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

#Prepares the username and password for the server protocol in order to authenticate the user
def AUTCommand(mySocket, username, password):
	
	msgSent = "AUT " + username + " " + password + "\n" 
	autRecv = ''

	sendMessage(mySocket, msgSent)
	
	autRecv = recvFixedMessage(mySocket).split(' ')

	if CMDMatcher(autRecv[0], "^AUR$"):
		status = autRecv[1]
		return status
					
def LSDCommand(mySocket):
	
	msgSent = "LSD\n"
	lsdRecv = ''
	
	sendMessage(mySocket, msgSent)
	lsdRecv = ((recvMessage(mySocket)).decode()).split(' ')

	if CMDMatcher(lsdRecv[0], '^LDR$'):
		msg = "Safe directories: " + lsdRecv[1] + "\n"
		for direc in lsdRecv[2:]:
			msg += direc + "\n"

		print(msg[:-2])

	return 1

def LSFCommand(mySocket, dir): #finish me later
	msgSent = "LSF " + dir
	sendMessage(mySocket, msgSent)

	lsfRecv = (recvMessage(mySocket).decode()).split(' ')

#The command that processes the Delete user request
def DLUCommand(mySocket):
		
	msgSent = 'DLU\n'
	dluRecv = ''

	sendMessage(mySocket,msgSent)
	dluRecv = recvFixedMessage(mySocket).split(' ')

	if CMDMatcher(dluRecv[0], "^DLR$"):
		print(dluRecv[1], end="")
		if CMDMatcher(dluRecv[1], "^OK\n$"):
			print("User deleted successfully")
			return 0;
		else:
			print("Couldn't delete user")
			return 1

def BCKCommand(mySocket, dir, username, password): #finish me later
	filenames = []
	msgSent = "BCK " + dir + ' '

	for dirpath, dirnames, files in os.walk("./" + dir):
		for filename in files:
			filenames += [filename]
			size = os.path.getsize(dir + '/' + filename)
			date = time.ctime(os.path.getmtime(dir + '/' + filename))
			msgSent += filename + ' ' + date + ' ' + str(size) + '\n'

	print(msgSent)

def DELCommand(mySocket, dir):
	msgSent = "DEL " + dir

	sendMessage(mySocket, msgSent)
	delRcv = recvFixedMessage(mySocket).split()

	if CMDMatcher(delRcv[0], '^DDR$'):
		if CMDMatcher(delRcv[1], '^OK$'):
			print(dir + " deleted successfully")
		elif CMDMatcher(delRcv[1], '^NOK$'):
			print("Couldn't delete " + dir)
	else:
		msgSent = "ERR"
		sendMessage(mySocket, msgSent)

def RSTCommand(mySocket, dir, username, password):
	msgSent = 'RST ' + dir + '\n'

	print(msgSent)

	sendMessage(mySocket, msgSent)

	rstRecv = recvFixedMessage(mySocket).split(' ')

	if CMDMatcher(rstRecv[0], '^RSR$'):
		mySocket.close()

		mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		mySocket.connect((rstRecv[1], int(rstRecv[2])))

		AUTCommand(mySocket, username, password)

		msgSentBS = 'RSB ' + dir + '\n'
		sendMessage(mySocket, msgSentBS)

		rstRecv = b''
		rstRecv = recvMessage(mySocket).split()

		if CMDMatcher(rstRecv[0], b'^RBR$'):
			if CMDMatcher(rstRecv[1], b'^EOF$'):
				print("No directory found")
			elif CMDMatcher(rstRecv[1], b'ERR'):
				print("Error processing the request")
			else:
				if not os.path.exists(dir):
					os.makedirs(dir)
				msg = 'Number of files: ' + rstRecv[1].decode()
				for n in range(1, int(rstRecv[1].decode())+1):
					file = open(dir + '/' + rstRecv[3*n-1].decode(), 'wb')
					file.write(rstRecv[3*n+1])

				print(dir + " restored successfully")
