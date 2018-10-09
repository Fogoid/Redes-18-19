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
	
	if CMDMatcher(rstRecv[0], b'^RBR$'):
		if CMDMatcher(rstRecv[1], b'^EOF$'):
			print("No directory found")
		elif CMDMatcher(rstRecv[1], b'ERR'):
			print("Error processing the request")
		else:
			if not os.path.exists(directory):
				os.makedirs(directory)
			msg = 'Number of files: ' + rstRecv[1].decode()
			n = 0
			spot = 1
			while n != rstRecv[1].decode():
				file = open(directory + '/' + rstRecv[spot].decode(), 'wb')
				spot = writeFile(file, rstRecv, spot)
				n += 1
				spot += 1
			file.close()

			print(directory + " restored successfully")

def UPLCommand(mySocket, directory, filesInfoList, username, password)
	msgSent = ('UPL ' + directory + ' ' + filesInfoList[0]).encode()
	data = b''
	AUTCommand(mySocket, username, password)

	for n in range(1, filesInfoList[0]):
		data = readFilesData(directory, filesInfoList[n*4 - 3], filesInfoList[n*4])
		fileInfo = filesInfoList[n*4-3] + ' ' + filesInfoList[n*4-2] + ' ' + filesInfoList[n*4-1] + ' ' + filesInfoList[n*4]
		msgSent += ' ' + fileInfo.encode() + data

	sendMessage(mySocket, msgSent)
	uplRecv = recvMessage(mySocket, 0).split()

	if CMDMatcher(uplRecv[0], '^UPR$'):
		if CMDMatcher(uplRecv[1], '^OK$'):
			print("Directory backed up successfully")
		elif CMDMatcher(uplRecv[1], '^NOK$'):
			print("It wasn't possible to backup the directory")

def writeFile(file, msg, n):
	nbits = int(msg[n + 3])
	print(nbits)
	n = n + 4
	part = b''

	while (msg[n])[-5:-3] != b'EOF':
		part += msg[n]
		nbits -= len(msg[n])
		n += 1

	file.write(part)

	return n
 