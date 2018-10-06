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
	serverSocket.bind((socket.gethostname(), 80))
	serverSocket.listen(5)	
	(clientSocket, address) = serverSocket.accept()
	#os.fork()
	#if newPID == 0:
		#break

while 1 :
	msgRecv = mySocket.recv(buffersize)
	msgRecv = msgRecv.decode()

	if AUTCommand(msgRecv):
		Username = msgRecv[4:9]
		Password = msgRecv[10:18]
		if checkUser(Username,Password) != 'NOK':
			msgRecv = mySocket.recv(buffersize)
			msgRecv = msgRecv.decode()
			if msgRecv == 'DLU\n':
				DLUCommand(Username,Password)
			elif msgRecv[0:4] == 'BCK ':
				BCKCommand(msgRecv)
			elif msgRecv[0:4] == 'RST ':
				RSTCommand(msgRecv)
			elif msgRecv == 'LSD\n':
				LSDCommand(Username,Password)
			elif msgRecv[0:4] == 'LSF ':
				LSFCommand(msgRecv)
			elif msgRecv[0:4] == 'DEL ':
				DELCommand(msgRecv)
