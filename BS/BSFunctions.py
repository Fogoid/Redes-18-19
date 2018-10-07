import socket
import sys
import argparse
import re
from shutil import rmtree

def getConnectionDetails():

	parser = argparse.ArgumentParser(description='Get connection details to connect to server.')
	parser.add_argument('-b', metavar='BSport', type=int, default=59000, help='Well-know available port for the CS and user to connect to')
	parser.add_argument('-n', metavar='CSname', type=str, default='localhost', help='Name of the CS where the BS will connect to')
	parser.add_argument('-p', metavar='CSport', type=int, default=58032, help='Port from CS where the BS will connect to')

	connectionDetails = parser.parse_args()
	print((connectionDetails.n,connectionDetails.p))
	return (connectionDetails.n, connectionDetails.p)

#General regex command matcher
def CMDMatcher(msg, pattern):
	matcher = re.compile(pattern)
	if matcher.match(msg):
		return 1
	return 0


#--------------------------------------------------
# BS-User TCP Protocol Commands
#--------------------------------------------------

#Simple function that sends the specified message through TCP
def sendTCPMessage(User_Socket, msg):
	User_Socket.send(msg.encode())

#Sends a 'ERR' message
def sendTCPError(User_Socket,msg):
	sendTCPMessage(User_Socket,'ERR\n')

#Checks if the given user is valid and is loaded in the BS server's users.txt list
def verifyUser(message):

	if CMDMatcher(message, '^AUT\s[0-9]{5}\s[0-9 a-z]{8}\n$'):
		message = message.split(' ')
		user = message[1]
		password = message[2].rstrip('\n')

		if os.path.exists(user+'.txt'):
			with open(user+'.txt') as file:
				if file.readline() == password:
					return 1
	return 0


#User TCP authentication command
def AUTCommand(User_Socket,message):
	AUT_msg = ''
	if verifyUser(message):
		AUT_msg = 'AUR OK\n'
	else:
		AUT_msg = 'AUR NOK\n'
	sendTCPMessage(User_Socket,message)


def UPLCommand():
	return 0

def RSBCommand():
	return 0

#--------------------------------------------------
# BS-CS UDP Protocol Commands
#--------------------------------------------------

#Simple function that sends a UDP message
def sendUDPMessage(message,CS_Socket,address,port):
	message = ''.join(message)
	CS_Socket.sendto(LFD_msg.encode(),(address,port))


#Function that registers the BS server on the CS through UDP
def startBS(CS_Socket,address,port):

	register = 'REG '+address+' '+str(port)+'\n'
	msgRecv = ""
	centralServer = ''

	while 1:
		CS_Socket.sendto(register.encode(),(address,port))
		(msgRecv, centralServer) = CS_Socket.recvfrom(1024)
		msgRecv = msgRecv.decode()
		print(msgRecv)

		if msgRecv == "RGR OK\n":
			return 1
	return 0


#Responsible for handling the LSF request
def LSFCommand(msgRecv,CS_Socket,address,port):
	directory = msgRecv[2].rstrip('\n')
	LFD_msg = ''

	if os.path.exists(msgRecv[1]):
		(dirpath,dirnames,files) = os.walk("./" + msgRecv[1])
		if directory in dirnames:
				for filename in files:
					size = os.path.getsize(msgRecv[1]+'/'+directory + '/' + filename)
					date = dateFormatter(time.ctime(os.path.getmtime(msgRecv[1]+'/'+directory + '/' + filename)))
					LFD_msg += filename + ' ' + date + ' ' + str(size) + '\n'
		else:
			LFD_msg = 'ERR\n'	
	else:
			LFD_msg = 'ERR\n'	

	sendUDPMessage(LFD_msg,CS_Socket,address,port)
	return 0

#Responsible for handling the server LSU request, CS server
#requests a new user to be registered
def LSUCommand(msgRecv,CS_Socket,address,port):
	LUR_msg=''
	filename='user_'+msgRecv[1]+'.txt'

	if CMDMatcher(msgRecv[0]+msgRecv[1]+msgRecv[2], '^AUT\s[0-9]{5}\s[0-9 a-z]{8}\n$'):
		if not os.path.exists(filename):
			with open(filename) as file:
				file.write(msgRecv[2].rstrip('\n').encode()) 
			os.makedirs(msgRecv[1])
		else:
			LUR_msg = 'NOK\n'
	else:
		LUR_msg ='ERR\n'

	sendUDPMessage(LUR_msg,CS_Socket,address,port)
	return 0



#Responsible for handling the DLB request from the CS server
def DLBCommand(msgRecv,CS_Socket,address,port):
	DBR_msg = ''

	if os.path.exists(msgRecv[1]):
		directory = msgRecv[2].rstrip('\n')
		if os.path.exists(msgRecv[1]+'/'+directory):
			shutil.rmtree(msgRecv[1]+'/'+directory,ignore_errors=True)
			DBR_msg = 'OK\n'
		else:
			DBR_msg = 'NOK\n'
	else:
		DBR_msg = 'NOK\n'

	sendUDPMessage(DLB_msg,CS_Socket,address,port)
	return 0