import socket
import sys
import argparse

def getConnectionDetails():

	parser = argparse.ArgumentParser(description='Get connection details to connect to server.')
	parser.add_argument('-n', metavar='CSname', type=str, default='localhost', help='Gives the name of the address do connect')
	parser.add_argument('-p', metavar='CSport', type=int, default=58032, help='Gives the port the user will connect to')

	connectionDetails = parser.parse_args()
	print((connectionDetails.n,connectionDetails.p))
	return (connectionDetails.n, connectionDetails.p)
	
def authenticateUser(mySocket):

	userExample = 'XXXXX NNNNNNNN'

	while True: 
		userLogin = input()

		if(userLogin[0: len('login')] == 'login' and len(userLogin[len('login '):]) == len(userExample)):

			userName = userLogin[len('login '):len('login ') + 5]
			userPassword = userLogin[-len("NNNNNNNN"):]

			status = AUTCommand(mySocket, userName, userPassword)
			

			print(status)
			if status == 'OK\n':
				print("User login successful")
			elif status == 'NOK\n':
				print("Wrong password")
			else:
				print("Your user was created successfully")

			return (userName, userPassword, 0)

		elif userLogin == 'exit':
			return ("XXXXX", "NNNNNNNN", 1)
		
		else:
			print("Please insert login XXXXX NNNNNNNN\nXXXXX - Your login 5 digit number\nNNNNNNNN - Your 8 character long password")

def sendMessage(mySocket, msgSent):
	mySocket.send(msgSent.encode())

def recvMessage(mySocket):
	msgRecv = ''
	
	msgRecv = mySocket.recv(256).decode()
	
	print((msgRecv, "this was a received message"))
	return msgRecv

def AUTCommand(mySocket, username, password):
	
	msgSent = "AUT " + username + " " + password + "\n" 

	sendMessage(mySocket, msgSent)
	
	msgRecv = recvMessage(mySocket)

	if msgRecv[0: len("AUR")] == "AUR":
		status = msgRecv[len("AUR "):]
		return status
	

def LSDCommand(mySocket):
	
	msgSent = "LSD\n"
	
	sendMessage(mySocket, msgSent)
	msgRecv = recvMessage(mySocket)

	if msgRecv[0: len('LDR ')] == 'LDR ':
		print(msgRecv[4:], end='')

	return 1

#The command that processes the Delete user request
def DLUCommand(mySocket):
		
		msgSent = 'DLU\n'
		
		sendMessage(mySocket,msgSent)
		msgRecv = recvMessage(mySocket)

		if msgRecv[0: len("DLR ")] == "DLR ":
			print(msgRecv[len("DLR "):], end="")
			if msgRecv[len("DLR "):] == "OK\n":
				print(msgRecv[len("DLR "):])
				return 0;
		return 1;