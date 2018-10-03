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

			print("ola")
			userName = userLogin[len('login '):len('login ') + 5]
			userPassword = userLogin[-len("NNNNNNNN"):]

			status = AUTCommand(mySocket, userName, userPassword)
			

			if status == 'OK':
				print("User loggin successfull")
			elif status == 'NOK':
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
	
	data = mySocket.recv(128)

	print(data.decode())
	msgRecv += data.decode()

	return msgRecv

def AUTCommand(mySocket, username, password):
	
	msgSent = "AUT " + username + " " + password + "\n" 


	sendMessage(mySocket, msgSent)

	print(("ainda estou vivo", username, password))
	
	msgRecv = recvMessage(mySocket)

	print("ta tudo fodido")

	if msgRecv[0: len("AUR")] == "AUR":
		status = msgRecv[len("AUR "):]
		return status
	

def LSDCommand(mySocket, size):
	
	msgSent = "LSD\n"
	
	sendMessage(mySocket, msgSent)
	msgRecv = recvMessage(mySocket, msgSent)

	if msgRecv[0: len('LDR ')] == 'LDR ':
		print(msgRecv[4:], end='')

	return 1

#The command that processes the Delete user request
def DLUCommand(mySocket, size):
		
		msgSent = 'DLU\n'
		
		msgRecv = recvMessage(mySocket, size, msgSent)

		if msgRecv[0: len("DLR ")] == "DLR ":
			print(msgRecv[len("DLR "):], end="")
			if msgRecv[len("DLR "):] == "OK":
				print(msgRecv[len("DLR "):])
				return 0;
		return 1;