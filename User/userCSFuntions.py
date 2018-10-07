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
	lsdRecv = ((recvMessage(mySocket)).decode()).split(' ')

	if CMDMatcher(lsdRecv[0], '^LDR$'):
		msg = "Safe directories: " + lsdRecv[1] + "\n"
		for direc in lsdRecv[2:]:
			msg += direc + "\n"

		print(msg[:-2])

	return 1

def LSFCommand(mySocket, dir): #finish me later
	msgSent = "LSF " + dir
	sendMessage(mySocket, msgSent)

	lsfRecv = (recvMessage(mySocket).decode()).split(' ')

#The command that processes the Delete user request
def DLUCommand(mySocket):
		
	msgSent = 'DLU\n'
	dluRecv = ''

	sendMessage(mySocket,msgSent)
	dluRecv = recvFixedMessage(mySocket).split(' ')

	if CMDMatcher(dluRecv[0], "^DLR$"):
		print(dluRecv[1], end="")
		if CMDMatcher(dluRecv[1], "^OK\n$"):
			print("User deleted successfully")
			return 0;
		else:
			print("Couldn't delete user")
			return 1

def BCKCommand(mySocket, dir, username, password): #finish me later
	filenames = []
	msgSent = "BCK " + dir + ' '

	for dirpath, dirnames, files in os.walk("./" + dir):
		for filename in files:
			filenames += [filename]
			size = os.path.getsize(dir + '/' + filename)
			date = time.ctime(os.path.getmtime(dir + '/' + filename))
			msgSent += filename + ' ' + date + ' ' + str(size) + '\n'

	print(msgSent)

def DELCommand(mySocket, dir):
	msgSent = "DEL " + dir

	sendMessage(mySocket, msgSent)
	delRcv = recvFixedMessage(mySocket).split()

	if CMDMatcher(delRcv[0], '^DDR$'):
		if CMDMatcher(delRcv[1], '^OK$'):
			print(dir + " deleted successfully")
		elif CMDMatcher(delRcv[1], '^NOK$'):
			print("Couldn't delete " + dir)
	else:
		msgSent = "ERR"
		sendMessage(mySocket, msgSent)

def RSTCommand(mySocket, directory, username, password):
	msgSent = 'RST ' + directory + '\n'

	print(msgSent)

	sendMessage(mySocket, msgSent)

	rstRecv = recvFixedMessage(mySocket).split(' ')

	if CMDMatcher(rstRecv[0], '^RSR$'):
		mySocket.close()

		mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		mySocket.connect((rstRecv[1], int(rstRecv[2])))

		RSBCommand(mySocket, directory, username, password)
