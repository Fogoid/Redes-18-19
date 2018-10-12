import socket
import sys
import argparse
import re
import os
import time


#Try catches for initializing a TCP socket
def TCPSocket():
		try:
			TCP_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			TCP_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		except socket.error as e:
			print ('Error creating TCPSocket\nTerminating Process')
			sys.exit(1)
		return TCP_Socket

#Try catches for initializing a UDP socket
def UDPSocket():
	try:
		UDP_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		UDP_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	except socket.error as e:
		print ('Error creating UDPSocket\nTerminating Process')
		sys.exit(1)
	return UDP_Socket

def getConnectionDetails():
	parser = argparse.ArgumentParser(description='Get connection details to connect to server.')
	parser.add_argument('-n', metavar='CSname', type=str, default='localhost', help='Gives the name of the address do connect')
	parser.add_argument('-p', metavar='CSport', type=int, default=58011, help='Gives the port the user will connect to')

	connectionDetails = parser.parse_args()
	return (connectionDetails.n, connectionDetails.p)

def CMDMatcher(msg, pattern):
	matcher = re.compile(pattern)
	if matcher.match(msg):
		return 1
	return 0

def dateFormatter(date):
	date = date.split(' ')
	newDate = str("%02d" % int(date[2])) + '.' + str("%02d" % int(time.strptime(date[1], '%b').tm_mon)) + '.' + date[4] + ' ' + date[3]
	return newDate

def sendMessage(mySocket, msgSent):
	try:
		if not isinstance(msgSent, bytes):
			msgSent = msgSent.encode()
		mySocket.sendall(msgSent)
	except socket.error as e:
		print ('Error sending message from TCPSocket to CS\nTerminating Process')
		sys.exit(1)
	return 0

def recvMessage(mySocket, n):
	try:
		if n:
			msg = ''.encode()
			while True:
				data = mySocket.recv(2048)
				if not data:
					break
				msg += data
		else:
			msg = mySocket.recv(128).decode()
	except socket.error as e:
		print ('Error receiving message from TCPSocket sent by CS\nTerminating Process')
		sys.exit(1)
	return msg

def readFilesData(directory, filename, size):
	data = b''
	try:
		file = open('./' + directory + '/' + filename, 'rb')
	except (OSError, IOError) as e:
		print('Error reading the file:'+filename+'\n')
	data = file.read(size)
	file.close()

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

def getFileDetails(filename, directory):
	date_time = dateFormatter(str(time.ctime(os.path.getmtime("./" + directory))))
	size = os.path.getsize("./" + directory + "/" + filename)
	return filename + ' ' + date_time + ' ' + str(size)

def authenticateUser(mySocket):

	while True:
		userLogin = input()

		if(CMDMatcher(userLogin,'^login\s[0-9]{5}\s[0-9 A-Z a-z]{8}$')):

			(cmd, username, password) = userLogin.split(' ')

			status = AUTCommand(mySocket, username, password)

			if status == 'OK\n':
				print("User login successful")
			elif status == 'NOK\n':
				print("Wrong password")
				continue
			elif status == 'NEW\n':
				print("A new user was created with your credentials")
			else:
				print("Error processing request")
				return ('NNNNNN', "NNNNNNNN", 1)

			return (username, password, 0)

		elif CMDMatcher(userLogin, '^exit$'):
			return ("NNNNN", "NNNNNNNN", 1)
		else:
			print("Please insert login XXXXX NNNNNNNN\nXXXXX - Your login 5 digit number\nNNNNNNNN - Your 8 character long password")

#Prepares the username and password for the server protocol in order to authenticate the user
def AUTCommand(mySocket, username, password):

	msgSent = "AUT " + username + " " + password + "\n"
	autRecv = ''

	sendMessage(mySocket, msgSent)

	autRecv = recvMessage(mySocket, 0).split(' ')

	if CMDMatcher(autRecv[0], "^AUR$"):
		status = autRecv[1]
		return status