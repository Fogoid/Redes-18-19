from userBaseFunctions import recvFixedMessage
from userBaseFunctions import CMDMatcher
from userBaseFunctions import sendMessage
import sys
import socket

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
	
	autRecv = recvFixedMessage(mySocket).split(' ')

	if CMDMatcher(autRecv[0], "^AUR$"):
		status = autRecv[1]
		return status
	