import sys 
import socket
import json
from userFunctions import *

#Creates a socket with a given protocol to establish a connection
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with open('userJSON.json') as file:
	data = json.load(file)

if len(data["CSname"]) == 0 :
	addressName = 'localhost'
else:
	addressName = data["CSname"]


if len(data["CSport"]) == 0 :
	port = 58032
else:
	port = int(float(data["CSport"]))

#gets the IPV4 correspondent to the addressName
address = socket.gethostbyname(addressName)
#has the maximum size of the buffer
buffersize = 230;

#connects the socket to the given adress and port
mySocket.connect((address, port))

login_success = 0;

messageRecv = ''
messageSent = input()

login_username = ''
login_password = ''

while messageSent != 'exit':
	messageRecv = ''

	#First login case in the User-CS protocol. Meant to login and introduce the pseudo "switch" case.
	if login_success==0 and messageSent[0:len('login')] == 'login' :

		messageSent = 'AUT' + messageSent[len('login'):] + "\n"
		mySocket.send(messageSent.encode())
		
		messageRecv = mySocket.recv(buffersize)
		messageRecv = messageRecv.decode()

		if messageRecv[0:len('AUR')] == 'AUR' :
			print(messageRecv[len('AUR') +1:], end='')

		if messageRecv[len('AUR') +1:] != 'NOK' :
			login_username = messageSent[len('login')-1:len('login')+5]
			login_password = messageSent[len('login')+5:len('login ')+14]
			login_success=1;

	#Should delete user if there are no dictories stored in the BS server
	elif messageSent == 'deluser' and login_success:
		login_success = DLUCommand()

	elif messageSent[0:len('backup ')] == 'backup '  and login_success:
		print(' ', end="")

	elif messageSent[0:len('restore ')] == 'restore ' and login_success:
		print(' ', end="")

	elif messageSent == 'dirlist' and login_success:
		login_success = LSDCommand(mySocket, buffersize)
		#messageSent = login_username + ' ' + login_password /***FIX ME***/
		#mySocket.send(messageSent.encode())				/***FIX ME***/ [Errno 32] Broken Pipe

	elif messageSent[0:len('filelist ')] == 'filelist ' and login_success:
		print(' ', end="")

	elif messageSent[0:len('delete ')] == 'delete ' and login_success:
		print(' ', end="")

	elif messageSent == 'logout' and login_success:
		login_success = 0;

	messageSent = input()

mySocket.close()
