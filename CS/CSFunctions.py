#Piece of code responsible for constantly dealing with the
#BS UDP connections
import re

def UDPConnections():

	print('Eu existo e cenas, obrigado por tudo pai')
	file = open('backupServers.txt','w')
	file.write('Tejo e fixe\n')
	file.close()


def checkUser(username,password):

	file = open('utilizadores.txt','r')
	for line in file.readline():
		temporary = line.split(',')

		if username == temporary[0]:
			if password != temporary[1]:
				return 'NOK'
			return 'OK'
	return 'NEW'

def AUTMatcher(message):
	pattern = re.compile('^AUT\s[0-9]{5}\s[0-9 a-z]{8}\n$')

	if pattern.match(message) != None:
		return 1
	return 0