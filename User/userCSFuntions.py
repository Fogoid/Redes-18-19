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

def LSFCommand(mySocket, directory):
	msgSent = "LSF " + directory + '\n'
	sendMessage(mySocket, msgSent)

	lsfRecv = (recvMessage(mySocket, 1).decode()).split(' ')
	if CMDMatcher(lsfRecv[0], '^LFD$'):
		if not CMDMatcher(lsfRecv[1], '^NOK\n$'):
			msg = "Backup server ip: " + lsfRecv[1] + "\nBackup server port: " + lsfRecv[2] + "\nFiles stored: " + lsfRecv[3] + "\n"
			for n in range(1, int(lsfRecv[3])+1):
				msg += lsfRecv[4*n] + ' ' + lsfRecv[4*n+1] + ' ' + lsfRecv[4*n+2] +  ' ' + lsfRecv[4*n + 3] + '\n'
			print(msg)
		else:
			print("Could not access directory "+directory)
	return 0

#The command that processes the Delete user request
def DLUCommand(mySocket):

	msgSent = 'DLU\n'
	dluRecv = ''

	sendMessage(mySocket,msgSent)
	dluRecv = recvMessage(mySocket, 0).split(' ')

	if CMDMatcher(dluRecv[0], "^DLR$"):
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

	sendMessage(mySocket, msgSent)
	bckRecv = (recvMessage(mySocket, 1).decode()).split(' ')
	bckRecv[-1] = bckRecv[-1].strip('\n')
	
	if CMDMatcher(bckRecv[0], '^BKR$'):
		if CMDMatcher(bckRecv[1], '^EOF$'):
			print("Request cant be processed")
		elif CMDMatcher(bckRecv[1], '^ERR$'):
			print("Request not correctly formulated")
		else:
			mySocket.close()

			mySocket = TCPSocket()

			try:
				mySocket.connect((bckRecv[1], int(bckRecv[2])))
			except socket.gaierror as e:
				print("Error related to the address the Socket is connecting to "+str(e)+"\n Terminating Process")
				sys.exit(1)
			except socket.error as e:
				print("Error related to the address the Socket is connecting to "+str(e)+"\n Terminating Process")
				sys.exit(1)

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

	sendMessage(mySocket, msgSent)

	rstRecv = recvMessage(mySocket, 0).split(' ')

	if CMDMatcher(rstRecv[0], '^RSR$'):
		mySocket.close()

		mySocket = TCPSocket()

		try:
			mySocket.connect((rstRecv[1], int(rstRecv[2])))
		except socket.gaierror as e:
			print("Error related to the address the Socket is connecting to "+str(e)+"\n Terminating Process")
			sys.exit(1)
		except socket.error as e:
			print("Error related to the address the Socket is connecting to "+str(e)+"\n Terminating Process")
			sys.exit(1)

		RSBCommand(mySocket, directory, username, password)

