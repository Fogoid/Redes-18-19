import socket
import sys
import os
import time
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
	usernameDirectory = "user_"+username
	files_info = b''
	file_number = 0

	if CMDMatcher(message, '^RSB\s[a-z]+\n$'):
		message = message.split(' ')
		message[1] = message[1].rstrip('\n')
		for (paths, dirnames, files) in os.walk('./' +usernameDirectory+'/'+message[1]):
			for filename in files:
				size = os.path.getsize('./' +usernameDirectory+'/'+message[1]+ '/' + filename)
				date = dateFormatter(time.ctime(os.path.getmtime('./' +usernameDirectory+'/'+message[1] + '/' + filename)))
				data = readFileData(usernameDirectory+'/'+message[1], filename, size)
				temp_string = ' ' + filename + ' ' + str(date) + ' ' + str(size)
				files_info += temp_string.encode() + b' ' + data + b' '
				file_number+=1
	else:
		rbrMsg += b'ERR'

	file_number = str(file_number)
	rbrMsg +=  file_number.encode()+files_info+ b'\n'
	sendTCPMessage(userSocket, rbrMsg)
	return 0