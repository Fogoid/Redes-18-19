import sys 
import socket
import json
import os
import re
from CSFunctions import *

Username = ''
Password = ''
buffersize = 256
users = { '99999':'zzzzzzzz'}

#newPID = os.fork()
#if newPID == 0:
#	UDPConnections()
	

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while 1:
	newPID = 1
	serverSocket.bind(('localhost', 80))
	serverSocket.listen(5)	
	(clientSocket, address) = serverSocket.accept()
	#os.fork()
	#if newPID == 0:
		#break

msgRecv = mySocket.recv(buffersize)
msgRecv = msgRecv.decode()

if AUTMatcher(msgRecv):
	Username = msgRecv[4:9]
	Password = msgRecv[10:18]
	print(Username+' '+Password)
	mySocket.send('AUR NEW')