import socket
import sys
import os
import time
from BSBaseFunctions import *

def UPRCommand(message, username, userSocket):
	uprMsg = 'UPR '

	print(message, 'This is what i recv')

	if CMDMatcher(message[0], b'^UPL$'):
		if not os.path.exists('./user_' + username + '/' + message[1].decode()):
				os.makedirs('./user_' + username + '/' + message[1].decode())
		index = 3
		for n in range(0, int(message[2].decode())):
			file = open('./user_' + username + '/' + message[1].decode() + '/' + message[index].decode(), 'wb')
			index = writeFileData(file, message, index)
			file.close()
		uprMsg += 'OK\n'
			
	else:
		uprMsg +='NOK\n'

	sendTCPMessage(userSocket, uprMsg)
	return 0

def RSBCommand(message, username, userSocket):
	rbrMsg = b'RBR '
	usernameDirectory = "user_"+username
	files_info = b''
	file_number = 0

	if CMDMatcher(message, b'^RSB\s[a-z]+\n$'):
		message = message.decode().split(' ')
		message[1] = message[1].rstrip('\n')
		for (paths, dirnames, files) in os.walk('./' +usernameDirectory+'/'+message[1]):
			for filename in files:
				size = os.path.getsize('./' +usernameDirectory+'/'+message[1]+ '/' + filename)
				date = dateFormatter(time.ctime(os.path.getmtime('./' +usernameDirectory+'/'+message[1] + '/' + filename)))
				data = readFileData(usernameDirectory+'/'+message[1], filename, size)
				temp_string = ' ' + filename + ' ' + str(date) + ' ' + str(size)
				files_info += temp_string.encode() + b' ' + data
				file_number+=1
	else:
		rbrMsg += b'ERR'

	file_number = str(file_number)
	rbrMsg +=  file_number.encode()+files_info+ b'\n'
	sendTCPMessage(userSocket, rbrMsg)
	return 0