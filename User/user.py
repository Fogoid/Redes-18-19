#! /usr/bin/python3

import sys 
import socket
from userFunctions import *

#Creates a socket with a given protocol to establish a connection
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#has the maximum size of the buffer
buffersize = 230;

connectionDetails = getConnectionDetails()

#connects the socket to the given adress and port
mySocket.connect(connectionDetails)

login_success = 0;

msgRecv = ''
msgSent = input()

login_username = ''
login_password = ''

while msgSent != 'exit':
	msgRecv = ''

	#First login case in the User-CS protocol. Meant to login and introduce the pseudo "switch" case.
	if login_success==0 and msgSent[0:len('login')] == 'login' :

		msgSent = 'AUT' + msgSent[len('login'):] + "\n"
		mySocket.send(msgSent.encode())
		
		msgRecv = mySocket.recv(buffersize)
		msgRecv = msgRecv.decode()

		if msgRecv[0:len('AUR')] == 'AUR' :
			print(msgRecv[len('AUR') +1:], end='')

		if msgRecv[len('AUR') +1:] != 'NOK' :
			login_username = msgSent[len('login')-1:len('login')+5]
			login_password = msgSent[len('login')+5:len('login ')+14]
			login_success=1;

	#Should delete user if there are no dictories stored in the BS server
	elif msgSent == 'deluser' and login_success:
		login_success = DLUCommand()

	elif msgSent[0:len('backup ')] == 'backup '  and login_success:
		print(' ', end="")

	elif msgSent[0:len('restore ')] == 'restore ' and login_success:
		print(' ', end="")

	elif msgSent == 'dirlist' and login_success:
		login_success = LSDCommand(mySocket, buffersize)
		#msgSent = login_username + ' ' + login_password /***FIX ME***/
		#mySocket.send(msgSent.encode())				/***FIX ME***/ [Errno 32] Broken Pipe

	elif msgSent[0:len('filelist ')] == 'filelist ' and login_success:
		print(' ', end="")

	elif msgSent[0:len('delete ')] == 'delete ' and login_success:
		print(' ', end="")

	elif msgSent == 'logout' and login_success:
		login_success = 0;

	msgSent = input()

mySocket.close()