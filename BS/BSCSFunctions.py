import socket
import sys
import os
from BSBaseFunctions import *

#Function that registers the BS server on the CS through UDP
def startBS(CS_Socket,CS_address,CS_port,BS_address,BS_port):

	register = 'REG ' + BS_address + ' ' + str(BS_port)+'\n'
	msgRecv = ""
	centralServer = ''
	print(register)
	CS_Socket.sendto(register.encode(),(CS_address,CS_port))

	while True: 
		(data, centralServer) = CS_Socket.recvfrom(1024)
		if data:
			break 
	msgRecv = data.decode()
	
	print((msgRecv, 'comecei com esta mensagem'))

	CS_Socket.close()

	if CMDMatcher(msgRecv, "^RGR OK\n$"):
		return 1

	return 0

'''
	MISSING HANDLER FOR CTRL+C IN ORDER TO FINISH UDP CONNECTION
'''

#Responsible for handling the LSF (listfile dir) request
def LFDCommand(msgRecv, CS_Socket, address, port):
	lfdMsg = b'LFD '
	directory = msgRecv[2].rstrip('\n')
	lfdMsg += readDirectory(msgRecv[1], directory)
	print(lfdMsg)

	sendUDPMessage(lfdMsg, CS_Socket, address, port)
	return 0

#Responsible for handling the server LSU request, CS server
#requests a new user to be registered
def LURCommand(msgRecv, CS_Socket, address, port):
	lurMsg='LUR '
	filename='user_'+msgRecv[1]+'.txt'

	full_msg = msgRecv[0]+' '+msgRecv[1]+' '+msgRecv[2]
	if CMDMatcher(full_msg, '^LSU\s[0-9]{5}\s[0-9 a-z]{8}\n$'):
		if not os.path.exists(filename):
			with open(filename,'w') as file:
				file.write(msgRecv[2].rstrip('\n'))
			os.makedirs('user_'+msgRecv[1])
			lurMsg += 'OK\n'
		else:
			lurMsg += 'NOK\n'
	else:
		lurMsg ='ERR\n'

	sendUDPMessage(lurMsg, CS_Socket, address, port)
	return 0

#Responsible for handling the DLB request from the CS server (delete dir given by the user)
def DBRCommand(msgRecv, CS_Socket, address, port):
	dbrMsg = 'DBR '
	userDirectory = 'user_' + msgRecv[1]

	if os.path.exists(userDirectory):
		directory = msgRecv[2].rstrip('\n')
		if os.path.exists(userDirectory+'/'+directory):
			shutil.rmtree(userDirectory+'/'+directory,ignore_errors=True)
			dbrMsg += 'OK\n'
		else:
			dbrMsg += 'NOK\n'
	else:
		dbrMsg += 'NOK\n'

	sendUDPMessage(dbrMsg, CS_Socket, address, port)
	return 0

#Defines the CTRL+C handler
def exitGracefully(CS_Socket,CS_address,CS_port,BS_address,BS_port):
	register = 'UNR '+BS_address+' '+str(BS_port)+'\n'
	msgRecv = ""
	centralServer = ''

	while 1:
		CS_Socket.sendto(register.encode(),(CS_address,CS_port))
		(msgRecv, centralServer) = CS_Socket.recvfrom(1024)
		msgRecv = msgRecv.decode()
		print(msgRecv)

		if msgRecv == "UAR OK\n":
			return 1
	return 0