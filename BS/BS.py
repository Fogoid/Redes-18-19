import sys 
import socket
import re
import os
import signal
from BSFunctions import *

#Starting the UDP socket to register in the CS
(addressName, port) = getConnectionDetails()
address = socket.gethostbyname(addressName)
CS_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
startBS(CS_Socket,address,port)

#This part will be responsible for the user TCP protocol implementation
newPID = os.fork()
buffersize = 256



# ----------------------------------------------------------------------------------
# BS-User TCP requests while cicle
# ----------------------------------------------------------------------------------
while newPID!=0:
	User_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	User_Socket.bind((socket.gethostname(), 58011))
	User_Socket.listen(5)	
	(clientSocket, User_address) = User_Socket.accept()

	msgRecv = mySocket.recv(buffersize).decode()

	if AUTCommand(msgRecv):
		msgRecv = msgRecv.split(' ')
		username = msgRecv[1]

		msgRecv = mySocket.recv(buffersize).decode()

		if CMDMatcher(msgRecv[0],'^UPL$'):
				UPLCommand(msgRecv,User_Socket)

		elif CMDMatcher(msgRecv[0],'^RSB$'):
				RSBCommand(msgRecv,username,User_Socket)
		else:
			sendTCPError(CS_Socket,address,port)
	User_Socket.close()

	



#This piece of code is working but disable CTRL + C interrupt. Let's leave it in a comment for now.
# ----------------------------------------------------------------------------------
#def SIGINT_Handler(signum,frame):
#	register = 'UNR '+address+' '+str(port)+'\n'
#	msgRecv = ""
#	centralServer = ''
#
#	while 1:
#		CS_Socket.sendto(register.encode(),(address,port))
#		(msgRecv, centralServer) = CS_Socket.recvfrom(1024)
#		msgRecv = msgRecv.decode()
#		print(msgRecv)
#
#		if msgRecv == "UAR OK\n":
#			return 1
#	return 0
#
#signal.signal(signal.SIGINT,SIGINT_Handler)
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# BS-CS UDP requests while cicle
# ----------------------------------------------------------------------------------
while 1:
	(msgRecv, centralServer) = CS_Socket.recvfrom(1024) 
	msgRecv = msgRecv.decode()
	msgRecv.split(' ')

	if CMDMatcher(msgRecv[0],'^LSF$'):
				LSFCommand(msgRecv,CS_Socket,address,port)

	elif CMDMatcher(msgRecv[0],'^LSU$'):
				LSUCommand(msgRecv,CS_Socket,address,port)

	elif CMDMatcher(msgRecv[0],'^DLB$'):
				DLBCommand(msgRecv,CS_Socket,address,port)
	else:
		sendUDPError(CS_Socket,address,port)
