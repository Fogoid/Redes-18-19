import sys 
import socket
import re
import os
import signal
from BSBaseFunctions import CMDMatcher
from BSUserFunctions import *
from BSCSFunctions import *

#Starting the UDP socket to register in the CS
(BS_port, CS_addressName, CS_port) = getConnectionDetails()
CS_address = socket.gethostbyname(CS_addressName)
BS_address = socket.gethostbyname('localhost')
CS_Start_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
startBS(CS_Start_Socket,CS_address,CS_port,BS_address,BS_port)


global exit
exit = 0
#This part will be responsible for the user TCP protocol implementation
newPID = os.fork()
buffersize = 256



# ----------------------------------------------------------------------------------
# BS-User TCP requests while cicle
## ----------------------------------------------------------------------------------
while newPID!=0:
	BS_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	BS_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	BS_Socket.bind((BS_address, BS_port))
	BS_Socket.listen(5)
	(User_Socket, User_address) = BS_Socket.accept()

	print(User_address)
	msgRecv = User_Socket.recv(buffersize).decode()

	if AUTCommand(msgRecv,User_Socket):
		msgRecv = msgRecv.split(' ')
		username = msgRecv[1]

		msgRecv = User_Socket.recv(buffersize).decode()
		msgSplit = msgRecv.split(' ')

		print(msgRecv)
		if CMDMatcher(msgSplit[0],'^UPL$'):
				UPLCommand(msgRecv,User_Socket)

		elif CMDMatcher(msgSplit[0],'^RSB$'):
				RSBCommand(msgRecv,username,User_Socket)
		else:
			sendTCPError(CS_Socket,address,port)
	User_Socket.close()
	BS_Socket.close()

	



#This piece of code is working but disable CTRL + C interrupt. Let's leave it in a comment for now.
# ----------------------------------------------------------------------------------
#def SIGINT_Handler(signum,frame):
#	exit = 1
#	print(exit)
#	return 0


#signal.signal(signal.SIGINT,SIGINT_Handler)
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# BS-CS UDP requests while cicle
# ----------------------------------------------------------------------------------

CS_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
CS_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
CS_Socket.bind((BS_address, BS_port))

while 1:
	(msgRecv, centralServer) = CS_Socket.recvfrom(1024) 
	msgRecv = msgRecv.decode()
	msgRecv= msgRecv.split(' ')

	print(exit)

	if CMDMatcher(msgRecv[0],'^LSF$'):
				LURCommand(msgRecv,CS_Socket,CS_address,CS_port)

	elif CMDMatcher(msgRecv[0],'^LSU$'):
				LSUCommand(msgRecv,CS_Socket,CS_address,CS_port)

	elif CMDMatcher(msgRecv[0],'^DLB$'):
				DLBCommand(msgRecv,CS_Socket,CS_address,CS_port)

	elif exit ==1:
		exitGracefully(CS_Socket,CS_address,CS_port,BS_address,BS_port)
		break;
	else:
		sendUDPError(CS_Socket,CS_address,CS_port)
print("Exited gracefully")