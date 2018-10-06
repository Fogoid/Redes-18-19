import sys 
import socket
import re
import os
import signal
from BSFunctions import *

(addressName, port) = getConnectionDetails()

address = socket.gethostbyname(addressName)


#This part will be responsible for the user TCP protocol implementation
#while 1:
	#os.fork()
	#newPID = 1
	#if newPID == 0:
		#break
	#serverSocket.bind((socket.gethostname(), 80))
	#serverSocket.listen(5)	
	#(clientSocket, address) = serverSocket.accept()
	


CS_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
startBS(CS_Socket,address,port)

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

while 1:
	(msgRecv, centralServer) = CS_Socket.recvfrom(1024) 
	msgRecv = msgRecv.decode()
	msgRecv.split(' ')

	if CMDMatcher(msgRecv[0],'^LSF '):
				LSFCommand()

	elif CMDMatcher(msgRecv[0],'^LSU '):
				LSUCommand()

	elif CMDMatcher(msgRecv[0],'^DLB '):
				DLBCommand()
	else:
		SendError(CS_Socket,address,port)
