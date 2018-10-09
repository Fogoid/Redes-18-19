import socket
import sys
import os
from CSBaseFunctions import *
import random

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
	LSF_BS_msg = 'LSF ' + username
	BKR_BS_msg = b''

	usernameDirectory = "user_"+username
	BS_Server = ''

	if CMDMatcher(msgRecv, '^BCK\s[a-z]+\s[0-9]+\s'):
		msgRecv = msgRecv.split(' ')
		if os.path.exists('./' + usernameDirectory + '/' + msgRecv[1]):
			file = open('./' + usernameDirectory + '/' + msgRecv[1] + '/IP_port.txt','r')
			[address, port] = file.readline().split(' ')
			file.close()
			LSF_BS_msg += msgRecv[1]
			BKR_user_msg += communicateUDP(LSU_BS_msg, address, port, BS_Socket) #FIXME: missing some arguments 
		else:
			BSconnection = getBS()
			if BSconnection in open('./' + usernameDirectory + '/BS_Register.txt').read():
				LSF_BS_msg += msgRecv[1]
				[address, port] = BSconnection.split(' ')
				BKR_user_msg += communicateUDP(LSF_BS_msg, address, port, BS_Socket) #FIXME: missing some arguments
			else:
				[address, port] = BSconnection.split(' ')
				communicateUDP(LSU_BS_msg, address, port, BS_Socket) #FIXME: do next steps


	else:
		BKR_user_msg = 'ERR\n'

	print(BKR_user_msg)
	sendTCPMessage(userSocket, BKR_user_msg)
	return 0

def getBS(username):
	file = open('./backupServers.txt', 'r')
	count = 0
	line = file.readline()
	BSList = [line]
	while  line != EOF:
		BSList += file.readline() 
		count += 1

	file.close()
	return BSList[floor(random.random()*count)]

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