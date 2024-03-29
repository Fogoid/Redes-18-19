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
	BSSocket = UDPSocket()

	while True:

		serverSocket = TCPSocket()
		serverSocket.bind((CS_address, CS_port))
		serverSocket.listen(2)
		(userSocket, client_address) = serverSocket.accept()
		msgRecv = userSocket.recv(buffersize)
		msgRecv = msgRecv.decode()

		if AUTCommand(userSocket, msgRecv):
			msgRecv = msgRecv.split(' ')
			Username = msgRecv[1]
			Password = msgRecv[2].rstrip('\n')
			print(Username+' '+'User '+msgRecv[0].rstrip('\n')+' '+client_address[0]+' '+str(client_address[1]))

			msgRecv = b''
			while True:
				data = userSocket.recv(buffersize)
				if data[-1:] == b'\n' or not data:
					msgRecv += data
					break
				msgRecv += data

			msgRecv = msgRecv.decode()
			msgSplit = msgRecv.split(' ')
			if msgRecv!='':
				print(Username+' '+'User '+msgSplit[0].rstrip('\n')+' '+client_address[0]+' '+str(client_address[1]))

			if CMDMatcher(msgSplit[0],'^DLU\n$'):
				DLRCommand(Username,userSocket)

			elif CMDMatcher(msgSplit[0],'^BCK$'):
				BKRCommand(msgRecv,Username,Password,userSocket)

			elif CMDMatcher(msgSplit[0],'^RST$'):
				RSRCommand(msgRecv,Username,userSocket)

			elif CMDMatcher(msgSplit[0],'^LSD\n$'):
				LDRCommand(Username,userSocket)

			elif CMDMatcher(msgSplit[0],'^LSF$'):
				LFDCommand(msgRecv,Username,userSocket)

			elif CMDMatcher(msgSplit[0],'^DEL$'):
				DDRCommand(msgRecv,Username,userSocket)

			else:
				sendTCPMessage(userSocket, 'ERR\n')

		serverSocket.close()
		userSocket.close()
