import sys 
import socket
import json
import os
import re
from CSFunctions import *

Username = ''
Password = ''
buffersize = 256
CSport = getConnectionDetails()

newPID = os.fork()
if newPID == 0:
	UDPConnections(CSport)
	

#User_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#while 1:
	#User_Socket.bind((socket.gethostname(), 80))
	#User_Socket.listen(5)	
	#(clientSocket, address) = User_Socket.accept()
	#newPID = os.fork()
	#if newPID == 0:
		#break

while 1 :
	#msgRecv = User_Socket.recv(buffersize)
	#msgRecv = msgRecv.decode()
	msgRecv = input("First After While Input\n")

	if AUTCommand(msgRecv,User_Socket):

		msgRecv = msgRecv.split(' ')
		Username = msgRecv[1]
		Password = msgRecv[2]

		#msgRecv = User_Socket.recv(buffersize)
		#msgRecv = msgRecv.decode().split(' ')

		if CMDMatcher(msgRecv[0],'^DLU\n$'):
				DLUCommand(User_Socket,Username)

		elif CMDMatcher(msgRecv[0],'^BCK$'):
				BCKCommand(msgRecv)

		elif CMDMatcher(msgRecv[0],'^RST$'):
				RSTCommand(msgRecv,Username,User_Socket)

		elif CMDMatcher(msgRecv[0],'^LSD\n$'):
				LSDCommand(Username,Password)

		elif CMDMatcher(msgRecv[0],'^LSF$'):
				LSFCommand(msgRecv)

		elif CMDMatcher(msgRecv[0],'^DEL$'):
				DELCommand(msgRecv,Username,User_Socket)

		else:
			sendTCPMessage('ERR\n',User_Socket)
