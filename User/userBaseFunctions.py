import socket
import sys
import argparse
import re
import os
import time


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
	newDate = date[3] + '.' + str(strptime(date[1], '%b').tm_mon) + '.' + date[5] + ' ' + date[4]
	return newDate

def sendMessage(mySocket, msgSent):
	mySocket.send(msgSent.encode())

def recvMessage(mySocket, n):
	if n:
		msg = ''.encode()
		while True:
			data = mySocket.recv(8)
			if not data:
				break
			msg += data
	else:
		msg = mySocket.recv(128).decode()
		
	print((msg, "this was a received message"))
	return msg

def authenticateUser(mySocket):

	while True: 
		userLogin = input()
		
		if(CMDMatcher(userLogin,'^login\s[0-9]{5}\s[0-9 a-z]{8}$')):

			(cmd, username, password) = userLogin.split(' ')

			status = AUTCommand(mySocket, username, password)

			if status == 'OK\n':
				print("User login successful")
			elif status == 'NOK\n':
				print("Wrong password") 
				continue
			else:
				print("A new user was created with your credentials")

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
	