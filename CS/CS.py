import sys
import socket
import json
import os
import re
from CSBaseFunctions import *
from CSUserFunctions import *

Username = ''
Password = ''
buffersize = 256
CS_port = getConnectionDetails()
CS_address = socket.gethostbyname('localhost')
newPID = os.fork()

if newPID == 0:
	UDPConnections(CS_address,CS_port)
else:
	BSSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	BSSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	while True:

		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		serverSocket.bind((CS_address, CS_port))
		serverSocket.listen(2)
		(userSocket, client_address) = serverSocket.accept()
		msgRecv = userSocket.recv(buffersize)
		msgRecv = msgRecv.decode()

		if AUTCommand(userSocket, msgRecv):
			msgRecv = msgRecv.split(' ')
			Username = msgRecv[1]
			Password = msgRecv[2].rstrip('\n')
			print(Username+' '+msgRecv[0].rstrip('\n')+' '+client_address[0]+' '+str(client_address[1]))

			msgRecv = userSocket.recv(buffersize)
			msgRecv = msgRecv.decode()
			msgSplit = msgRecv.split(' ')
			if msgRecv!='':
				print(Username+' '+msgSplit[0].rstrip('\n')+' '+client_address[0]+' '+str(client_address[1]))

			if CMDMatcher(msgSplit[0],'^DLU\n$'):
				DLRCommand(Username,userSocket)

			elif CMDMatcher(msgSplit[0],'^BCK$'):
				BKRCommand(msgRecv,Username,Password,userSocket,BSSocket)

			elif CMDMatcher(msgSplit[0],'^RST$'):
				RSRCommand(msgRecv,Username,userSocket)

			elif CMDMatcher(msgSplit[0],'^LSD\n$'):
				LDRCommand(Username,userSocket)

			elif CMDMatcher(msgSplit[0],'^LSF$'):
				LFDCommand(msgRecv,Username,userSocket, BSSocket)

			elif CMDMatcher(msgSplit[0],'^DEL$'):
				DDRCommand(msgRecv,Username,userSocket)

			else:
				sendTCPMessage(userSocket, 'ERR\n')

		serverSocket.close()
		userSocket.close()
