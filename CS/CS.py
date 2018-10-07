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
	

#serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#while 1:
	#serverSocket.bind((socket.gethostname(), 80))
	#serverSocket.listen(5)	
	#(clientSocket, address) = serverSocket.accept()
	#newPID = os.fork()
	#if newPID == 0:
		#break

while 1 :
	#msgRecv = mySocket.recv(buffersize)
	#msgRecv = msgRecv.decode()
	msgRecv = input("First After While Input\n")

	if AUTCommand(msgRecv):

		msgRecv = msgRecv.split(' ')
		Username = msgRecv[1]
		Password = msgRecv[2]

		if checkUser(Username,Password) != 'NOK':
			#msgRecv = mySocket.recv(buffersize)
			#msgRecv = msgRecv.decode()

			if CMDMatcher(msgRecv[0],'^DLU\n$'):
				DLUCommand(Username,Password)

			elif CMDMatcher(msgRecv[0],'^BCK$'):
				BCKCommand(msgRecv)

			elif CMDMatcher(msgRecv[0],'^RST$'):
				RSTCommand(msgRecv)

			elif CMDMatcher(msgRecv[0],'^LSD\n$'):
				LSDCommand(Username,Password)

			elif CMDMatcher(msgRecv[0],'^LSF$'):
				LSFCommand(msgRecv)

			elif CMDMatcher(msgRecv[0],'^DEL$'):
				DELCommand(msgRecv)

			else:
				print("Did not recognize that command")
