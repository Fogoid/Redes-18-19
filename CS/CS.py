import sys 
import socket
import json
import os
from CSFunctions import *

userUsername = [99999]
userPassword = ['zzzzzzzz']
buffersize = 256

newPID = os.fork()
if newPID == 0:
	UDPConnections()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while 1:
	newPID = 1;
	serverSocket.bind(('localhost', 84))
	serverSocket.listen(5)	
	(clientSocket, address) = serverSocket.accept()
	os.fork()
	if newPID == 0:
		break

msgRecv = mySocket.recv(buffersize)
msgRecv = msgRecv.decode()
print(msgRecv)

if msgRecv[0:len('AUT ')] == 'AUT ':

	if msgRecv[4:9] == 99999 and msgRecv[11:19] == 'zzzzzzzz':
		mySocket.send('OK')
	else:
		mySocket.send('NOK')