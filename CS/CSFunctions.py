#Piece of code responsible for constantly dealing with the
#BS UDP connections
import re

def UDPConnections():

	print('Eu existo e cenas, obrigado por tudo pai')
	file = open('backupServers.txt','w')
	file.write('Tejo e fixe\n')
	file.close()

#General regex command matcher
def CMDMatcher(msg, pattern):
	matcher = re.compile(pattern)
	if matcher.match(msg):
		return 1
	return 0


#Checks if the user exists
def checkUser(username,password):

	file = open('utilizadores.txt','r')

	for line in file.readlines():
		temporary = line.split(' ')

		if username == temporary[0]:
			if password != temporary[1].rstrip('\n'):
				file.close()
				return 'NOK'
			file.close()
			return 'OK'

	file.close()
	file = open('utilizadores.txt','ab+')	
	package = username + ' ' + password + '\n'
	file.write(package.encode())
	file.close()
	return 'NEW'

#User authentication command
def AUTCommand(message):
	if CMDMatcher(message, '^AUT\s[0-9]{5}\s[0-9 a-z]{8}$'):
		return 1
	return 0


def DLUCommand(username,password):
	return 0

def BCKCommand(msgRecv):
	return 0

def RSTCommand(msgRecv):
	return 0

def LSDCommand(username,password):
	return 0

def LSFCommand(msgRecv):
	return 0

def DELCommand(msgRecv):
	return 0