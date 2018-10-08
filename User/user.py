#! /usr/bin/python3

import sys 
import socket
import re
from userBaseFunctions import *
from userCSFuntions import *

(addressName, port) = getConnectionDetails()

address = socket.gethostbyname(addressName)

exit = 0
loggedIn = 0

while not exit:

	if loggedIn:
		cmd = input()
		cmd = cmd.split(' ')

	#Creates a socket with a given protocol to establish a connection
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	
	if not loggedIn:
		mySocket.connect((address, port))
		
		(userName, userPassword, exit) = authenticateUser(mySocket)

		loggedIn = 1

		mySocket.close()
		continue
		
	else:
		if not (CMDMatcher(cmd[0], '^logout$') or CMDMatcher(cmd[0],'^exit$')):
			mySocket.connect((address, port))
			AUTCommand(mySocket, userName, userPassword)

	if exit:
		break

	#First login case in the User-CS protocol. Meant to login and introduce the pseudo "switch" case.
	#Should delete user if there are no dictories stored in the BS server

	if CMDMatcher(cmd[0],'^deluser$'):
		loggedIn = DLUCommand(mySocket)

	elif CMDMatcher(cmd[0],'^backup$'):
		BCKCommand(mySocket, cmd[1], userName, userPassword)

	elif CMDMatcher(cmd[0],'^restore$'):
		RSTCommand(mySocket, cmd[1], userName, userPassword)

	elif CMDMatcher(cmd[0],'^dirlist$'):
		LSDCommand(mySocket)

	elif CMDMatcher(cmd[0],'^filelist$'):
		LSFCommand(mySocket, cmd[1])

	elif CMDMatcher(cmd[0],'^delete$'):
		DELCommand(mySocket, cmd[1])

	elif CMDMatcher(cmd[0], '^logout$'):
		loggedIn = 0
	
	elif CMDMatcher(cmd[0],'^exit$'):
	 	exit = 1

	if not (CMDMatcher(cmd[0], '^logout$') or CMDMatcher(cmd[0],'^exit$')):
		mySocket.close()