#! /usr/bin/python3

import sys 
import socket
from userFunctions import *

(addressName, port) = getConnectionDetails()

address = socket.gethostbyname("tejo.tecnico.ulisboa.pt")

exit = 0
loggedIn = 0

while not exit:

	#Creates a socket with a given protocol to establish a connection
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	mySocket.connect((address, port))
	
	if not loggedIn:

		(userName, userPassword, exit) = authenticateUser(mySocket)
	
		loggedIn = 1

	else:
		AUTCommand(mySocket, userName, userPassword)

	if exit:
		break
	else:
		command = input()

	#First login case in the User-CS protocol. Meant to login and introduce the pseudo "switch" case.
	#Should delete user if there are no dictories stored in the BS server

	if command == 'deluser' and loggedIn:
		loggedIn = DLUCommand(mySocket)

	elif command[0:len('backup ')] == 'backup '  and loggedIn:
		print(' ', end="")

	elif command[0:len('restore ')] == 'restore ' and loggedIn:
		print(' ', end="")

	elif command == 'dirlist' and loggedIn:
		LSDCommand(mySocket)

	elif command[0:len('filelist ')] == 'filelist ' and loggedIn:
		print(' ', end="")

	elif command[0:len('delete ')] == 'delete ' and loggedIn:
		print(' ', end="")

	elif command == 'logout':
		loggedIn = 0
	
	elif command == 'exit':
		exit = 1

	mySocket.close()
	