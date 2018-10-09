import socket
import sys
import os
from CSBaseFunctions import *

def DLRCommand(username, userSocket):
	dlrMsg = 'DLR '

	usernameDirectory = 'user_'+username

	if os.path.exists(usernameDirectory):
		for dirpath, dirnames, files in os.walk("./" + usernameDirectory):
			if(len(dirnames)==0):
				removeUser(username)
				dlrMsg +='OK\n'
				break
	else:
		dlrMsg +='NOK\n'

	sendTCPMessage(userSocket, dlrMsg)
	return 0

def BKRCommand(msgRecv, username, password, userSocket, BS_Socket):

	BKR_user_msg ='BKR '
	LSU_BS_msg = 'LSU' + ' ' + username + ' ' + password
	BKR_BS_msg = ''

	usernameDirectory = "user_"+username
	BS_Server = ''
	register = 1

	if CMDMatcher(msgRecv, '^BCK\s[a-z]+\s[0-9]+\s'):
		msgRecv = msgRecv.split(' ')
		if os.path.exists(usernameDirectory+'/'+msgRecv[1]):
			if os.path.exists(usernameDirectory+'/'+msgRecv[1]+'/'+'IP_port.txt'):
				with open(usernameDirectory+'/'+msgRecv[1]+'/'+'IP_port.txt','r') as file:
					BS_Server = file.readline()
					BKR_user_msg+=BS_Server + '\n' 
		else:
			os.makedirs('./'+usernameDirectory+'/'+msgRecv[1])
			with open("backupServers.txt",'r') as BS_file:
				with open(usernameDirectory+'/'+msgRecv[1]+'/'+'IP_port.txt','w') as user_file:
					BS_Server = BS_file.readline()
					user_file.write(BS_Server)
					BKR_user_msg+=BS_Server + '\n'
			with open('./'+usernameDirectory+'/'+'BS_Register.txt','r') as bs_file:
				for line in bs_file.readlines():
					if line == BS_Server:
						register = 0
			if register == 1:
				with open('./'+usernameDirectory+'/'+'BS_Register.txt','a+') as bs_file:
					bs_file.write(BS_Server)
					BS_Server = BS_Server.split(' ')
					BS_Server[1] = BS_Server[1].rstrip('\n')
					communicateUDP(LSU_BS_msg,BS_Server[0],BS_Server[1],BS_Socket)

	else:
		BKR_user_msg = 'ERR\n'

	print(BKR_user_msg)
	sendTCPMessage(userSocket, BKR_user_msg)
	return 0

def RSRCommand(msgRecv, username, userSocket):

	rsrMsg ='RSR '
	usernameDirectory = "user_"+username

	if CMDMatcher(msgRecv, '^RST\s[a-z]+\n$'):
		msgRecv = msgRecv.split(' ')
		directory = msgRecv[1].rstrip('\n')
		if os.path.exists('./'+usernameDirectory+'/'+directory):
			with open('./'+usernameDirectory+ '/' + directory + '/' + 'IP_port.txt','r') as file:
				 rsrMsg += file.readline()+'\n'
		else:
			rsrMsg += 'EOF\n'
	else:
		rsrMsg = 'ERR\n'

	sendTCPMessage(userSocket, rsrMsg)
	return 0

def LDRCommand(username, userSocket):

	ldrMsg ='LDR '
	dirnameList = ''
	usernameDirectory = "user_"+username
	n = 0

	if os.path.exists(usernameDirectory):
		for dirpath, dirnames, files in os.walk("./" + usernameDirectory):
			for name in dirnames:
				n += 1
				dirnameList += ' ' +name

	ldrMsg += str(n) + dirnameList + '\n'
	sendTCPMessage(userSocket, ldrMsg)
	return 0

def LFDCommand(msgRecv, username, userSocket):
	lfdMsg='LFD '
	usernameDirectory = "user_" + username

	if CMDMatcher(msgRecv, '^LSF\s[a-z]+\n$'):
		msgRecv=msgRecv.split(' ')
		msgRecv[1] = msgRecv[1].rstrip('\n')
		if os.path.exists(usernameDirectory + '/' + msgRecv[1]):
			with open(usernameDirectory+'/'+msgRecv[1]+'/'+'IP_port.txt','r') as file:
				bs_data = file.readline().split(' ')
				BS_Server.append(bs_data[0])
				BS_Server.append(bs_data[1])
			lfdMsg += BS_Server[0]+' '
			lfdMsg += BS_Server[1]+' '
	else:
		lfdMsg='ERR\n'

	sendTCPMessage(lfdMsg, userSocket)
	return 0

def DDRCommand(msgRecv,username,userSocket):
	ddrMsg = 'DDR '
	usernameDirectory = "user_" + username
	BS_Server = []

	if CMDMatcher(msgRecv, '^DEL\s[a-z]+\n$'):
		msgRecv=msgRecv.split(' ')
		msgRecv[1] = msgRecv[1].rstrip('\n')
		if os.path.exists(usernameDirectory+'/'+msgRecv[1]):
			with open(usernameDirectory+'/'+msgRecv[1]+'/'+'IP_port.txt','r') as file:
				bs_data = file.readline().split(' ')
				BS_Server.append(bs_data[0])
				BS_Server.append(bs_data[1])
			#FIX ME : SEND BS SERVER INSTRUCTION TO DESTROY DIR
			shutil.rmtree(usernameDirectory+'/'+msgRecv[1],ignore_errors=True)
			ddrMsg += 'OK\n'
		else:
			ddrMsg += 'NOK\n'
	else:
		ddrMsg='ERR\n'
	sendTCPMessage(userSocket, ddrMsg)
	return 0