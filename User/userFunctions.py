import socket
import sys
import argparse
import re

def getConnectionDetails():

	parser = argparse.ArgumentParser(description='Get connection details to connect to server.')
	parser.add_argument('-n', metavar='CSname', type=str, default='localhost', help='Gives the name of the address do connect')
	parser.add_argument('-p', metavar='CSport', type=int, default=58032, help='Gives the port the user will connect to')

	connectionDetails = parser.parse_args()
	print((connectionDetails.n,connectionDetails.p))
	return (connectionDetails.n, connectionDetails.p)
	
def CMDMatcher(msg, pattern):
	matcher = re.compile(pattern)
	if matcher.match(msg):
		return 1
	return 0

def authenticateUser(mySocket):

	while True: 
		userLogin = input()
		print(userLogin.encode())
		if(CMDMatcher(userLogin,'^login\s[0-9]{5}\s[0-9 a-z]{8}$')):

			(cmd, username, password) = userLogin.split(' ')

			status = AUTCommand(mySocket, username, password)

			print(status)
			if status == 'OK\n':
				print("User login successful")
			elif status == 'NOK\n':
				print("Wrong password") 
				continue
			else:
				print("A new user was created with your credentials")

			cmd = input()
			return (username, password, 0, cmd)

		elif userLogin == 'exit':
			return ("NNNNN", "NNNNNNNN", 1, "none")
		else:
			print("Please insert login XXXXX NNNNNNNN\nXXXXX - Your login 5 digit number\nNNNNNNNN - Your 8 character long password")

def sendMessage(mySocket, msgSent):
	mySocket.send(msgSent.encode())

def recvMessage(mySocket):
	msgRecv = ''
	
	msgRecv = mySocket.recv(256).decode()
	
	print((msgRecv, "this was a received message"))
	return msgRecv

#Prepares the username and password for the server protocol in order to authenticate the user
def AUTCommand(mySocket, username, password):
	
	msgSent = "AUT " + username + " " + password + "\n" 
	sendMessage(mySocket, msgSent)
	msgRecv = recvMessage(mySocket).split(' ')

	if CMDMatcher(msgRecv[0], "^AUR$"):
		status = msgRecv[1]
		return status
	

def LSDCommand(mySocket):
	
	msgSent = "LSD\n"
	sendMessage(mySocket, msgSent)
	msgRecv = recvMessage(mySocket).split(' ')

	if CMDMatcher(msgRecv[0], '^LDR$'):
		msg = "Safe directories: " + msgRecv[1] + "\n"
		for direc in msgRecv[2:]:
			msg += direc + "\n"

		print(msg)

	return 1

#The command that processes the Delete user request
def DLUCommand(mySocket):
		
		msgSent = 'DLU\n'
		sendMessage(mySocket,msgSent)
		msgRecv = recvMessage(mySocket).split(' ')

		print(msgRecv)
		if CMDMatcher(msgRecv[0], "^DLR$"):
			print(msgRecv[1], end="")
			if CMDMatcher(msgRecv[1], "^OK\n$"):
				print("User deleted successfully")
				return 0;
			else:
				print("Couldn't delete user")
				return 1