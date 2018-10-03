#! /usr/bin/python3

import sys 
import socket
from userFunctions import *

#Creates a socket with a given protocol to establish a connection
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

(addressName, port) = getConnectionDetails()

address = socket.gethostbyname("tejo.tecnico.ulisboa.pt")

exit = 0
loggedIn = 0

while not exit:

	if not loggedIn:
		mySocket.connect((address, 58011))

		(userName, userPassword, exit) = authenticateUser(mySocket)
		
		mySocket.close()

		loggedIn = 1

	else:
		mySocket.connect((address, 58011))
		print("AINDA NAO ESTOU MORTO CARALHO")
		AUTCommand(mySocket, userName, userPassword)

		if exit:
			break

		#First login case in the User-CS protocol. Meant to login and introduce the pseudo "switch" case.
		#Should delete user if there are no dictories stored in the BS server

		if command == 'deluser' and login_success:
			login_success = DLUCommand()

		elif command[0:len('backup ')] == 'backup '  and login_success:
			print(' ', end="")

		elif command[0:len('restore ')] == 'restore ' and login_success:
			print(' ', end="")

		elif command == 'dirlist' and login_success:
			login_success = LSDCommand(mySocket, buffersize)

		elif command[0:len('filelist ')] == 'filelist ' and login_success:
			print(' ', end="")

		elif command[0:len('delete ')] == 'delete ' and login_success:
			print(' ', end="")

		elif command == 'logout':
			loggedIn = 0
		
		elif command == 'exit':
			exit = 1

		mySocket.close()

		if not exit:
			command = input()