import socket
import sys
import os
from BSBaseFunctions import *

def UPRCommand(message, username, userSocket):
	uprMsg = 'UPR '

	if CMDMatcher(message, '^UPL\s[a-z]+[0-9]+\s'):
		uprMsg += writeDirectory(message, username)
	else:
		uprMsg +='NOK\n'

	sendTCPMessage(userSocket, uprMsg)
	return 0

def RSBCommand(message, username, userSocket):
	rbrMsg = b'RBR'
	if CMDMatcher(message, '^RSB\s[a-z]+\n$'):
		message = message.split(' ')
		for (paths, dirnames, files) in os.walk('./' + message[1]):
			for filename in files:
				size = os.path.getsize('./' + message[1] + '/' + filename)
				date = dateFormatter(time.ctime(os.path.getmtime(usernameDirectory+'/'+directory + '/' + filename)))
				data = readFileData(message[1], filename, size)
				rbrMsg += (' ' + filename + ' ' + date + ' ' + size).encode() + data
	else:
		rbrMsg += b'ERR'

	rbrMsg += b'\n'
	sendTCPMessage(userSocket, rbrMsg)
	return 0