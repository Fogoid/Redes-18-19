import sys 
import socket
import json
from userFunctions import *

#Creates a socket with a given protocol to establish a connection
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with open('userJSON.json') as file:
	data = json.load(file)

if(data["CSname"] == ""):
	addressName = 'localhost'
else:
	addressName = data["CSname"]


if(data["CSport"] == "")
	port = 58032
else:
	port = data["CSport"]

#gets the IPV4 correspondent to the addressName
address = socket.gethostbyname(addressName)
#has the maximum size of the buffer
buffersize = 230;

#connects the socket to the given adress and port
mySocket.connect((address, port))

#Makes the autentication of the user
message = input()

if (message[0:len('login')] == 'login'):
	mySocket.send(message.encode())
	
	message = mySocket.recv(buffersize)

	print(message.decode())

	#Checks the following operation if a new user was created or if he was successfully authenticated
	message = input()

	if(message == 'dirlist'):
		LSDCommand()

	mySocket.send(message.encode())

else:
	mySocket.close()


mySocket.close()