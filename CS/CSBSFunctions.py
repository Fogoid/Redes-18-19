import socket
import sys
import os
from CSBaseFunctions import *

def LSFCommand(BSSocket, BSIP, BSport, username, dirname):
	lsfMsg = 'LSF ' + username + ' ' + dirname + '\n'
	print(("morro aqui?"))
	msgRecv = communicateUDP(lsfMsg, BSIP, BSport, BSSocket)
	splitedMsg = msgRecv.split(' ')
	if CMDMatcher(msgRecv, '^LFD\s[0-9]\s'):
		if len(splitedMsg[2:]) == 4*splitedMsg[1]:
			return splitedMsg[1:]
	elif CMDMatcher(msgRecv, '^ERR$'):
		return 'ERR'

def LSUCommand(BSSocket, BSIP, BSport, username, password):
	lsuMsg = 'LSU ' + username + ' ' + password + '\n'
	msgRecv = communicateUDP(lsuMsg, BSIP, BSport, BSSocket)
	print(("LSU received this msg:", msgRecv))
	splitedMsg = msgRecv.split(' ')
	if CMDMatcher(msgRecv, '^LUR\s[A-Z]\n$'):
		return splitedMsg[1]
	elif CMDMatcher(msgRecv, '^ERR\n$'):
		return 'ERR'
