import sys 
import socket
import json
import os
import re
from CSFunctions import *

Username = ''
Password = ''
buffersize = 256
CS_port = getConnectionDetails()
CS_address = socket.gethostbyname('localhost')
newPID = os.fork()

if newPID == 0:
	UDPConnections(CS_address,CS_port)

	
#while 1:
	#newPID = os.fork()
	#if newPID == 0:
		#break
else:
	while 1: 	
		Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		Server_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		Server_Socket.bind((CS_address, CS_port))
		Server_Socket.listen(2)	
		(User_Socket, client_address) = Server_Socket.accept()
		msgRecv = User_Socket.recv(128)
		msgRecv = msgRecv.decode()

		if AUTCommand(msgRecv,User_Socket):

			msgRecv = msgRecv.split(' ')
			Username = msgRecv[1]
			Password = msgRecv[2].rstrip('\n')
			

			msgRecv = User_Socket.recv(buffersize)
			msgRecv = msgRecv.decode()
			msgRecv = msgRecv.split(' ')
			print(Username+' '+msgRecv[0].rstrip('\n')+' '+client_address[0]+' '+str(client_address[1]))

			if CMDMatcher(msgRecv[0],'^DLU\n$'):
				DLUCommand(Username,User_Socket)

			elif CMDMatcher(msgRecv[0],'^BCK$'):
				BCKCommand(msgRecv,Username,Password,User_Socket)

			elif CMDMatcher(msgRecv[0],'^RST$'):
				RSTCommand(msgRecv,Username,User_Socket)

			elif CMDMatcher(msgRecv[0],'^LSD\n$'):
				LSDCommand(Username,User_Socket)

			elif CMDMatcher(msgRecv[0],'^LSF$'):
				LSFCommand(msgRecv,Username,User_Socket)

			elif CMDMatcher(msgRecv[0],'^DEL$'):
				DELCommand(msgRecv,Username,User_Socket)

			else:
				sendTCPMessage('ERR\n',User_Socket)

		Server_Socket.close()
		User_Socket.close()	