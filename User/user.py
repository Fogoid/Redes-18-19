#! /usr/bin/python3

import sys 
import socket
import re
from userFunctions import *

(addressName, port) = getConnectionDetails()

address = socket.gethostbyname("tejo.tecnico.ulisboa.pt")

exit = 0
loggedIn = 0

while not exit:

	if loggedIn:
		cmd = input()

	#Creates a socket with a given protocol to establish a connection
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	mySocket.connect((address, port))
	
	if not loggedIn:
		(userName, userPassword, exit, cmd) = authenticateUser(mySocket)

		loggedIn = 1

	if exit:
		break

	#First login case in the User-CS protocol. Meant to login and introduce the pseudo "switch" case.
	#Should delete user if there are no dictories stored in the BS server

	cmd = cmd.split(' ')
	
	if CMDMatcher(cmd[0],'^deluser$') and loggedIn:
		AUTCommand(mySocket, userName, userPassword)
		loggedIn = DLUCommand(mySocket)

	elif CMDMatcher(cmd[0],'^backup$') and loggedIn:
		AUTCommand(mySocket, userName, userPassword)
		print(' ', end="")

	elif CMDMatcher(cmd[0],'^restore$') and loggedIn:
		AUTCommand(mySocket, userName, userPassword)
		print(' ', end="")

	elif CMDMatcher(cmd[0],'^dirlist$') and loggedIn:
		AUTCommand(mySocket, userName, userPassword)
		LSDCommand(mySocket)

	elif CMDMatcher(cmd[0],'^filelist$') and loggedIn:
		AUTCommand(mySocket, userName, userPassword)
		print(' ', end="")

	elif CMDMatcher(cmd[0],'^delete$') and loggedIn:
		AUTCommand(mySocket, userName, userPassword)
		print(' ', end="")

	elif CMDMatcher(cmd[0], '^logout$'):
		loggedIn = 0
	
	elif CMDMatcher(cmd[0],'^exit$'):
	 	exit = 1

	mySocket.close()