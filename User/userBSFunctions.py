import os
import sys
import socket
from userBaseFunctions import *

def RSBCommand(mySocket, directory, username, password):
	
	AUTCommand(mySocket, username, password)

	msgSentBS = 'RSB ' + directory + '\n'
	sendMessage(mySocket, msgSentBS)

	rstRecv = b''
	rstRecv = recvMessage(mySocket, 1).split()

	if CMDMatcher(rstRecv[0], b'^RBR$'):
		if CMDMatcher(rstRecv[1], b'^EOF$'):
			print("No directory found")
		elif CMDMatcher(rstRecv[1], b'ERR'):
			print("Error processing the request")
		else:
			if not os.path.exists(directory):
				os.makedirs(directory)
			msg = 'Number of files: ' + rstRecv[1].decode()
			for n in range(1, int(rstRecv[1].decode())+1):
				file = open(directory + '/' + rstRecv[3*n-1].decode(), 'wb')
				file.write(rstRecv[3*n+1])

			print(directory + " restored successfully")

 