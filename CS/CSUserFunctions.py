import socket
import sys
import os
from CSBaseFunctions import *
from CSBSFunctions import *
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

def BKRCommand(msgRecv, username, password, userSocket):

	BKR_user_msg ='BKR '
	LSF_BS_msg = ''
	usernameDirectory = "user_"+username
	BS_Server = ''
	status = 'NOK'

	print(msgRecv)
	print("dont i receive the whole thing?")
	splitedMsg = msgRecv.split(' ')

	if CMDMatcher(splitedMsg[0], '^BCK$'):
		if os.path.exists('./' + usernameDirectory + '/' + splitedMsg[1]):
			file = open('./' + usernameDirectory + '/' + splitedMsg[1] + '/IP_port.txt','r')
			[address, port] = file.readline().split(' ')
			file.close()
			LSF_BS_msg += splitedMsg[1]
			filesKept = LSFCommand(address, port, username, splitedMsg[1])
			common = notCommon(splitedMsg[2:], filesKept[1:])
			BKR_user_msg += len(common)
			for string in common:
				BKR_user_msg += ' ' + string
			BKR_user_msg += '\n'
		else:
			BSconnection = getBS()
			[BSIP, BSport] = BSconnection.split(' ')
			file = open('./' + usernameDirectory + '/BS_Register.txt')
			while True:
				if file.readline() == BSconnection:
					status = "OK\n"
					break
				elif file.readline() == '':
					status = LSUCommand(BSIP, BSport, username, password)
					break
			file.close()

			if not os.path.exists('./' + usernameDirectory + '/' + splitedMsg[1]):
				os.makedirs('./' + usernameDirectory + '/' + splitedMsg[1])
			file = open('./' + usernameDirectory + '/' + splitedMsg[1] + '/IP_port.txt', 'w')
			file.write(BSconnection.strip('\n'))
			file.close()
			
			file = open('./' + usernameDirectory + '/BS_Register.txt', 'w')
			file.write(BSconnection.strip('\n'))
			file.close()

			if CMDMatcher(status, '^OK\n$'):
				BKR_user_msg += BSconnection.strip('\n') + ' ' + ' '.join(splitedMsg[2:])
			else:
				BKR_user_msg += 'ERR\n'
	else:
		BKR_user_msg = 'ERR\n'

	print(BKR_user_msg)
	sendTCPMessage(userSocket, BKR_user_msg)
	return 0

 #AUXILIARY FUNCTIONS
def notCommon(list1, list2):
	files1 = []
	files2 = []

	for i in range(0, int(list1[0])):
		files1 += [' '.join(x for x in list1[i*4+1:i*4+5])]
	for i in range(0, int(list2[0])):
		files2 += [' '.join(x for x in list2[i*4+1:i*4+5])]
	print(files1, files2)
	return getNotCommon(files1, files2, [])

def getNotCommon(list1, list2, notCommon):
	if list1 == []:
		return notCommon
	elif not list1[0] in list2:
		return getNotCommon(list1[1:], list2, notCommon + [list1[0]])
	else:
		return getNotCommon(list1[1:], list2, notCommon)

def getBS():
	file = open('./backupServers.txt', 'r')
	msg = file.readline()
	#FIXME for more BS
	file.close()

	return msg

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

def LFDCommand(msgRecv, username, userSocket, BSSocket):
	lfdMsg='LFD '
	usernameDirectory = "user_" + username
	msgRecv = msgRecv.split(' ')
	BS_Server = []
	if CMDMatcher(msgRecv[0], '^LSF$') and len(msgRecv) < 3:
		existsInBS = 0
		msgRecv[1] = msgRecv[1].rstrip('\n')
		if os.path.exists(usernameDirectory + '/' + msgRecv[1]):
			with open(usernameDirectory+'/'+msgRecv[1]+'/'+'IP_port.txt','r') as file:
				bs_data = file.readline().split(' ')
				BS_Server.append(bs_data[0])
				BS_Server.append(bs_data[1])
			lfdMsg += BS_Server[0] + ' '
			lfdMsg += BS_Server[1] + ' '
			lfdMsg += LSFCommand(BSSocket, BS_Server[0], BS_Server[1], username, msgRecv[1])
			print(lfdMsg)
	else:
		lfdMsg='ERR\n'

	sendTCPMessage(userSocket, lfdMsg)
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
