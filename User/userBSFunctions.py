import os
import sys
import socket
from userBaseFunctions import *

def RSBCommand(mySocket, directory, username, password):
	
	AUTCommand(mySocket, username, password)

	msgSentBS = 'RSB ' + directory + '\n'
	sendMessage(mySocket, msgSentBS)

	rstRecv = b''
	rstRecv = recvMessage(mySocket, 1).split(b' ')
	rstRecv[-1] = (rstRecv[-1])[:-1]
	
	if CMDMatcher(rstRecv[0], b'^RBR$'):
		if CMDMatcher(rstRecv[1], b'^EOF$'):
			print("No directory found")
		elif CMDMatcher(rstRecv[1], b'ERR'):
			print("Error processing the request")
		else:
			if not os.path.exists(directory):
				os.makedirs(directory)
			msg = 'Number of files: ' + rstRecv[1].decode()
			index = 2
			for n in range(0, int(rstRecv[1].decode())):
				file = open('./' + directory + '/' + rstRecv[index].decode(), 'wb')
				index = writeFileData(file, rstRecv, index)
				file.close()

			print(directory + " restored successfully")

def UPLCommand(mySocket, directory, filesInfoList, username, password):
	msgSent = 'UPL ' + directory + ' ' + filesInfoList[0]
	msgSent = msgSent.encode()
	data = b''
	AUTCommand(mySocket, username, password)

	for n in range(1, int(filesInfoList[0])+1):
		data = readFilesData(directory, filesInfoList[n*4 - 3], int(filesInfoList[n*4]))
		fileInfo = filesInfoList[n*4-3] + ' ' + filesInfoList[n*4-2] + ' ' + filesInfoList[n*4-1] + ' ' + filesInfoList[n*4]
		msgSent += b' ' + fileInfo.encode() + data

	print(msgSent)
	sendMessage(mySocket, msgSent)
	uplRecv = recvMessage(mySocket, 0).split()

	if CMDMatcher(uplRecv[0], '^UPR$'):
		if CMDMatcher(uplRecv[1], '^OK$'):
			print("Directory backed up successfully")
		elif CMDMatcher(uplRecv[1], '^NOK$'):
			print("It wasn't possible to backup the directory")

 