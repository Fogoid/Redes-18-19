import socket
import sys
import argparse
import re
import os
import time
from shutil import rmtree


#Try catches for initializing a TCP socket
def TCPSocket():
		try:
			TCP_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			TCP_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		except socket.error as e:
			print ('Error creating socket: '+ e + '\nTerminating Process')
			sys.exit(1)
		return TCP_Socket

#Try catches for initializing a UDP socket
def UDPSocket():
	try:
		UDP_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		UDP_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	except socket.error as e:
		print ('Error creating socket: '+ e + '\nTerminating Process')
		sys.exit(1)
	return UDP_Socket

def getConnectionDetails():

	parser = argparse.ArgumentParser(description='Get connection details to connect to server.')
	parser.add_argument('-b', metavar='BSport', type=int, default=59000, help='Well-know available port for the CS and user to connect to')
	parser.add_argument('-n', metavar='CSname', type=str, default='localhost', help='Name of the CS where the BS will connect to')
	parser.add_argument('-p', metavar='CSport', type=int, default=58011, help='Port from CS where the BS will connect to')

	connectionDetails = parser.parse_args()
	return (connectionDetails.b,connectionDetails.n, connectionDetails.p)

#General regex command matcher
def CMDMatcher(msg, pattern):
	matcher = re.compile(pattern)
	if matcher.match(msg):
		return 1
	return 0

#Simple function that puts the date in the right format
def dateFormatter(date):
	date = date.split(' ')
	newDate = str("%02d" % int(date[2])) + '.' + str("%02d" % int(time.strptime(date[1], '%b').tm_mon)) + '.' + date[4] + ' ' + date[3]
	return newDate

#Function gets all data from a file
def readFileData(directory, filename, size):
	data = b''

	try:
		file = open('./' + directory + '/' + filename, 'rb')
		data = file.read(size)
		file.close()
	except (OSError, IOError) as e:
		print('Error reading the file:'+filename+'\n')
	

	return data

#Writes data on a file
def writeFileData(file, dataList, i):
	size = int(dataList[i+3].decode())
	i += 4
	data = dataList[i]

	while len(data) != size:
		i += 1
		data += b' ' + dataList[i]

	file.write(data)

	return i + 1

def readDirectory(username, directory):
	usernameDirectory = "user_" + username
	msg = b''

	for (dirpath, dirnames, files) in os.walk("./" + usernameDirectory + '/' + directory):
		msg += str(len(files)).encode()
		for filename in files:
			size = os.path.getsize(usernameDirectory+'/'+directory + '/'+filename)
			date = dateFormatter(time.ctime(os.path.getmtime(usernameDirectory+'/'+directory + '/' + filename)))
			msg += b' ' + filename.encode() + b' ' + date.encode() + b' ' + str(size).encode()
		msg += b'\n'
	return msg


#Simple function that sends the specified message through TCP
def sendTCPMessage(User_Socket, msg):
	try:
		if not isinstance(msg, bytes):
			msg = msg.encode()
		User_Socket.sendall(msg)
	except socket.error as e:
		print ('Error sending message from TCPSocket to User \nTerminating Process')
		sys.exit(1)
	return 1


#Sends a 'ERR' message
def sendTCPError(User_Socket,msg):
	sendTCPMessage(User_Socket,'ERR\n')

#User TCP authentication command
def AUTCommand(message,User_Socket):
	AUT_msg = ''
	if verifyUser(message):
		AUT_msg = 'AUR OK\n'
	else:
		AUT_msg = 'AUR NOK\n'
	sendTCPMessage(User_Socket,AUT_msg.encode())

	if AUT_msg != 'NOK\n':
		return 1
	return 0

#Checks if the given user is valid and is loaded in the BS server's users.txt list
def verifyUser(message):

	if CMDMatcher(message, '^AUT\s[0-9]{5}\s[0-9 A-Z a-z]{8}\n$'):
		message = message.split(' ')
		user_file = 'user_' + message[1] +'.txt'
		password = message[2].rstrip('\n')

		if os.path.exists(user_file):
			with open(user_file,'r') as file:
				if file.readline() == password:
					return 1
	return 0

#Simple function that sends a UDP message
def sendUDPMessage(message,CS_Socket,address,port):
	try:
		if not isinstance(message, bytes):
			message = message.encode()
			CS_Socket.sendto(message,(address,port))
	except socket.error as e:
		print ('Error sending message from UDPSocket to CS  \nTerminating Process')
		sys.exit(1)
	return 1
