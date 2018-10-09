#Piece of code responsible for constantly dealing with the
#BS UDP connections
import re
import socket
import sys
import argparse
import os
import shutil 

def getConnectionDetails():

	parser = argparse.ArgumentParser(description='Get connection details')
	parser.add_argument('-p', metavar='CSport', type=int, default=58011, help='Gives the port the user will connect to')

	connectionDetails = parser.parse_args()
	print(connectionDetails.p)
	return connectionDetails.p

#General regex command matcher
def CMDMatcher(msg, pattern):
	matcher = re.compile(pattern)
	if matcher.match(msg):
		return 1
	return 0

#Simple function that sends the specified message through TCP
def sendTCPMessage(msg,User_Socket):
	User_Socket.send(msg.encode())

#Simple function that communicates in TCP
def communicateUDP(msg,BS_information):
	BS_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	BS_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	BS_information = BS_information.split(' ')
	BS_Socket.sendto(msg,(BS_information[0], int(BS_information[1].rstrip('\n'))))
	(msgRecv, BS_Server) = BS_Socket.recvfrom(1024)
	print(msgRecv)	


#Cicle that keeps waiting for new BS's to register
def UDPConnections(CS_address,CS_port):
	BS_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	BS_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	BS_Socket.bind((CS_address, CS_port))	
	BS_Server = ''	
	msgRecv =''

	while 1:
	

		(msgRecv, BS_Server) = BS_Socket.recvfrom(1024)
		print(BS_Server)
		msgRecv = msgRecv.decode().split(' ')
		print(msgRecv)
		RGR_msg = 'RGR '
		if CMDMatcher(msgRecv[0],'^REG$') and CMDMatcher(msgRecv[2],'^[0-9]{5}\n$'):
			file = open('backupServers.txt','ab+')
			file.write((msgRecv[1] + ' '+ msgRecv[2]).encode())
			file.close()
			RGR_msg+='OK\n'
		else:
			RGR_msg+='NOK\n'
		BS_Socket.sendto(RGR_msg.encode(),(BS_Server[0],int(BS_Server[1])))
	BS_Socket.close()
	return 0



#Function that eliminates the user from the list of users
def removeUser(username):
	os.remove('user_'+username+'.txt')
	shutil.rmtree('user_'+username,ignore_errors=True)
	return 1

#User authentication command
def AUTCommand(message,User_Socket):
	AUT_msg = ''
	if CMDMatcher(message, '^AUT\s[0-9]{5}\s[0-9 a-z]{8}$'):
		message = message.split(' ')
		datafile = 'user_'+message[1] + '.txt'
		password = message[2].rstrip('\n')
		if os.path.exists(datafile):
			with open(datafile,'r') as file:
				if file.readline().rstrip('\n') == password.rstrip('\n'):
					AUT_msg = 'OK\n'
				else:
					AUT_msg = 'NOK\n'
		else:
			with open(datafile,'w') as file:
				file.write(password)
			os.makedirs('user_'+message[1])
			file = open('user_'+message[1]+'/'+'BS_Register.txt','w') 
			file.close()	
			AUT_msg = 'NEW\n'
	else:
		AUT_msg = 'ERR\n'

	sendTCPMessage(AUT_msg,User_Socket)

	if AUT_msg != 'ERR\n' and AUT_msg != 'NOK\n':
		return 1
	return 0


def DLUCommand(username,User_Socket):
	DLR_msg = 'DLR '

	username_directory = 'user_'+username

	if os.path.exists(username_directory):
		for dirpath, dirnames, files in os.walk("./" + username_directory):
			if(len(dirnames)==0):
				removeUser(username)
				DLR_msg +='OK\n'
				break
	else:
		DLR_msg +='NOK\n'

	sendTCPMessage(DLR_msg,User_Socket)
	return 0

def BCKCommand(msgRecv,username,password,User_Socket):

	BKR_user_msg ='BKR '
	LSU_BS_msg = 'LSU' + ' ' + username + ' ' + password
	BKR_BS_msg = ''

	username_directory = "user_"+username
	BS_Server = ''
	register = 1

	if CMDMatcher(msgRecv, '^BKR\s[a-z]+\s[0-9]+\s'):
		msgRecv = msgRecv.split(' ')
		if os.path.exists(username_directory+'/'+msgRecv[1]):
			if os.path.exists(username_directory+'/'+msgRecv[1]+'/'+'IP_port.txt'):
				with open(username_directory+'/'+msgRecv[1]+'/'+'IP_port.txt','r') as file:
					BS_Server = file.readline()
					BKR_user_msg+=BS_Server + ' ' 
		else:
			os.makedirs('./'+username_directory+'/'+msgRecv[1])
			with open("backupServers.txt",'r') as BS_file:
				with open(username_directory+'/'+msgRecv[1]+'/'+'IP_port.txt','w') as user_file:
					BS_Server = BS_file.readline()
					user_file.write(BS_Server)
					BKR_user_msg+=BS_Server + ' '
			with open('./'+username_directory+'/'+'BS_Register.txt','r') as bs_file:
				for line in bs_file.readlines():
					if line == BS_Server:
						register = 0
			if register == 1:
				with open('./'+username_directory+'/'+'BS_Register.txt','ab+') as bs_file:
					bs_file.write(BS_Server)
					communicateUDP(LSU_BS_msg,BS_Server)

	else:
		BKR_user_msg = 'ERR\n'


	sendTCPMessage(User_Socket,BKR_user_msg)
	return 0

def RSTCommand(msgRecv,username,User_Socket):

	RSR_msg ='RSR '
	if CMDMatcher(msgRecv, '^RST\s[a-z]+\n$'):
		msgRecv=msgRecv.split(' ')
		if os.path.exists('user_'+username+'/'+msgRecv[1]):
			with open('user_'+username+'/'+msgRecv[1]+'/'+'IP_port.txt','r') as file:
				 RSR_msg += file.readline()+'\n'
		else:
			RSR_msg += 'EOF\n'
	else:
		RSR_msg='ERR\n'

	sendTCPMessage(User_Socket,RSR_msg)
	return 0

def LSDCommand(username,User_Socket):

	LDR_msg ='LDR '
	dirnameList = ''
	username_directory = "user_"+username
	n = 0

	if os.path.exists(username_directory):
		for dirpath, dirnames, files in os.walk("./" + username_directory):
			for name in dirnames:
				n += 1
				dirnameList += name+' '

	LDR_msg += str(n) + ' ' + dirnameList + '\n'
	sendTCPMessage(LDR_msg,User_Socket)
	return 0

def LSFCommand(msgRecv,username,User_Socket):
	LFD_msg='LFD '
	username_directory = "user_"+username


	if CMDMatcher(msgRecv, '^LSF\s[a-z]+\n$'):
		msgRecv=msgRecv.split(' ')
		msgRecv[1] = msgRecv[1].rstrip('\n')
		if os.path.exists(username_directory+'/'+msgRecv[1]):
			with open(username_directory+'/'+msgRecv[1]+'/'+'IP_port.txt','r') as file:
				bs_data = file.readline().split(' ')
				BS_Server.append(bs_data[0])
				BS_Server.append(bs_data[1])
			LFD_msg += BS_Server[0]+' '
			LFD_msg += BS_Server[1]+' '
	else:
		LFD_msg='ERR\n'

	sendTCPMessage(User_Socket,LFD_msg)
	return 0

def DELCommand(msgRecv,username,User_Socket):
	DDR_msg = 'DDR '
	username_directory = "user_"+username
	BS_Server = []


	if CMDMatcher(msgRecv, '^DEL\s[a-z]+\n$'):
		msgRecv=msgRecv.split(' ')
		msgRecv[1] = msgRecv[1].rstrip('\n')
		if os.path.exists(username_directory+'/'+msgRecv[1]):
			with open(username_directory+'/'+msgRecv[1]+'/'+'IP_port.txt','r') as file:
				bs_data = file.readline().split(' ')
				BS_Server.append(bs_data[0])
				BS_Server.append(bs_data[1])
			#FIX ME : SEND BS SERVER INSTRUCTION TO DESTROY DIR
			shutil.rmtree(username_directory+'/'+msgRecv[1],ignore_errors=True)
			DDR_msg += 'OK\n'
		else:
			DDR_msg += 'NOK\n'
	else:
		DDR_msg='ERR\n'
	sendTCPMessage(User_Socket,DDR_msg)
	return 0