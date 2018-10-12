import sys
import socket
import re
import os
import signal
from BSBaseFunctions import CMDMatcher
from BSUserFunctions import *
from BSCSFunctions import *

#Starting the UDP socket to register in the CS
global global_CS_addressName, global_CS_port, global_BS_address, global_BS_port

(BS_port, CS_addressName, CS_port) = getConnectionDetails()
CS_address = socket.gethostbyname(CS_addressName)
BS_address = socket.gethostbyname('localhost')
CS_Start_Socket = UDPSocket()
exit = startBS(CS_Start_Socket,CS_address,CS_port,BS_address,BS_port)
global_CS_addressName = CS_address
global_CS_port = CS_port
global_BS_address = BS_address
global_BS_port =  BS_port


exit = 0
#This part will be responsible for the user TCP protocol implementation
newPID = os.fork()
buffersize = 8192



# ----------------------------------------------------------------------------------
# BS-User TCP requests while cicle
## ----------------------------------------------------------------------------------
if newPID == 0:
	while True:

		BS_Socket = TCPSocket()
		BS_Socket.bind((BS_address, BS_port))
		BS_Socket.listen(5)
		try:
			(User_Socket, User_address) = BS_Socket.accept()
		except (KeyboardInterrupt, SystemExit) as e:
			print("The Keyboard interruption CTRL+C was pressed. Will soon exit.")
			sys.exit(1)

		msgRecv = User_Socket.recv(buffersize).decode()

		if AUTCommand(msgRecv,User_Socket):

			msgRecv = msgRecv.split(' ')
			username = msgRecv[1]

			msgRecv = b''
			data = b''
			while True:
				data = User_Socket.recv(buffersize)
				msgRecv += data
				if msgRecv[-1:] == b'\n':
					break

			msgSplit = msgRecv.split(b' ')
			msgSplit[-1] = msgSplit[-1].strip(b'\n')

			if CMDMatcher(msgSplit[0],b'^UPL$'):
					UPRCommand(msgSplit,username, User_Socket)

			elif CMDMatcher(msgSplit[0],b'^RSB$'):
					RSBCommand(msgRecv,username,User_Socket)
			else:
				sendTCPError(User_Socket,address,port)

		User_Socket.close()
		BS_Socket.close()





#This piece of code is working but disable CTRL + C interrupt. Let's leave it in a comment for now.
# ----------------------------------------------------------------------------------
def SIGINT_Handler(signum,frame):

	udp_socket = UDPSocket()
	message = 'UNR '+ global_BS_address + ' ' + str(global_BS_port) + '\n'
	sendUDPMessage(message,udp_socket,global_CS_addressName,global_CS_port)
	(message, server) = udp_socket.recvfrom(1024)
	message = message.decode()
	if CMDMatcher(message,'^UAR OK\n$'):
		print("Terminating process")
		sys.exit(1)
	print(message)
	return 0


signal.signal(signal.SIGINT,SIGINT_Handler)
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# BS-CS UDP requests while cicle
# ----------------------------------------------------------------------------------

CS_Socket = UDPSocket()
CS_Socket.bind((BS_address, BS_port))

while 1:
	(msgRecv, centralServer) = CS_Socket.recvfrom(1024)
	msgRecv = msgRecv.decode()
	msgRecv= msgRecv.split(' ')
	CS_address = centralServer[0]
	CS_port = centralServer[1]

	if CMDMatcher(msgRecv[0],'^LSF$'):
				LFDCommand(msgRecv,CS_Socket,CS_address,CS_port)

	elif CMDMatcher(msgRecv[0],'^LSU$'):
				LURCommand(msgRecv,CS_Socket,CS_address,CS_port)

	elif CMDMatcher(msgRecv[0],'^DLB$'):
				DBRCommand(msgRecv,CS_Socket,CS_address,CS_port)

	elif exit ==1:
		exitGracefully(CS_Socket,CS_address,CS_port,BS_address,BS_port)
		break;
	#else:
		#sendUDPError(CS_Socket,CS_address,CS_port)
print("Exited gracefully")
