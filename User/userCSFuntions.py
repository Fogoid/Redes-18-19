from userBaseFunctions import *
from userBSFunctions import *
import os
import time
import sys
import socket

def LSDCommand(mySocket):
	
	msgSent = "LSD\n"
	lsdRecv = ''
	
	sendMessage(mySocket, msgSent)
	lsdRecv = ((recvMessage(mySocket, 1)).decode()).split(' ')

	if CMDMatcher(lsdRecv[0], '^LDR$'):
		msg = "Safe directories: " + lsdRecv[1] + "\n"
		for direc in lsdRecv[2:]:
			msg += direc + "\n"

		print(msg[:-2])

	return 1

def LSFCommand(mySocket, directory): #finish me later
	msgSent = "LSF " + directory
	sendMessage(mySocket, msgSent)

	lsfRecv = (recvMessage(mySocket, 1).decode()).split(' ')

	if CMDMatcher(lsfRecv[0], '^LFD$'):
		msg = "Backup server ip: " + lsfRecv[1] + "\nBackup server port: " + lsfRecv[2] + "\nFiles stored: " + lsfRecv[3] + "\n"
		for n in range(1, lsfRecv[3]+1):
			msg += lsfRecv[3*n+1:3*n+3]
		print(msg)

#The command that processes the Delete user request
def DLUCommand(mySocket):
		
	msgSent = 'DLU\n'
	dluRecv = ''

	sendMessage(mySocket,msgSent)
	dluRecv = recvMessage(mySocket, 0).split(' ')

	if CMDMatcher(dluRecv[0], "^DLR$"):
		print(dluRecv[1], end="")
		if CMDMatcher(dluRecv[1], "^OK\n$"):
			print("User deleted successfully")
			return 0;
		else:
			print("Couldn't delete user")
			return 1

def BCKCommand(mySocket, directory, username, password):
	msgSent = "BCK " + directory + ' '
	filesNumber = 0
	filesInfo = ''

	for dirpath, dirnames, files in os.walk("./" + directory):
		for filename in files:
			filesInfo += ' ' + getFileDetails(filename, directory)
			filesNumber += 1

	msgSent += str(filesNumber) + filesInfo + '\n'

	print(msgSent)

	sendMessage(mySocket, msgSent)
	bckRecv = (recvMessage(mySocket, 1).decode()).split(' ')

	if CMDMatcher(bckRecv[0], '^BKR$'):
		if CMDMatcher(bckRecv[1], '^EOF$'):
			print("Request cant be processed")
		elif CMDMatcher(bckRecv[1], '^ERR$'):
			print("Request not correctly formulated")
		else:
			mySocket.close()

			mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			mySocket.connect((bckRecv[1], int(bckRecv[2])))

			UPLCommand(mySocket, directory, bckRecv[3:], username, password)

def DELCommand(mySocket, directory):
	msgSent = "DEL " + directory + '\n'

	sendMessage(mySocket, msgSent)
	delRcv = recvMessage(mySocket, 0).split()

	if CMDMatcher(delRcv[0], '^DDR$'):
		if CMDMatcher(delRcv[1], '^OK$'):
			print(directory + " deleted successfully")
		elif CMDMatcher(delRcv[1], '^NOK$'):
			print("Couldn't delete " + directory)
	else:
		msgSent = "ERR"
		sendMessage(mySocket, msgSent)

def RSTCommand(mySocket, directory, username, password):
	msgSent = 'RST ' + directory + '\n'

	print(msgSent)

	sendMessage(mySocket, msgSent)

	rstRecv = recvMessage(mySocket, 0).split(' ')

	if CMDMatcher(rstRecv[0], '^RSR$'):
		mySocket.close()

		mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		mySocket.connect((rstRecv[1], int(rstRecv[2])))

		RSBCommand(mySocket, directory, username, password)
