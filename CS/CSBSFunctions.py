import socket
import sys
import os
from CSBaseFunctions import *

def LSFCommand(BSIP, BSport, username, dirname):
	lsfMsg = 'LSF ' + username + ' ' + dirname + '\n'
	msgRecv = communicateUDP(lsfMsg, BSIP, BSport)
	splitedMsg = msgRecv.split(' ')
	if CMDMatcher(splitedMsg[0], '^LFD$'):
		if len(splitedMsg[2:]) == 4*int(splitedMsg[1]):
			return msgRecv[4:]
	elif CMDMatcher(msgRecv, '^ERR$'):
		return 'ERR'

def LSUCommand(BS_IP, BS_port, username, password):
	lsuMsg = 'LSU ' + username + ' ' + password + '\n'
	msgRecv = communicateUDP(lsuMsg, BS_IP, BS_port)
	splitedMsg = msgRecv.split(' ')
	if CMDMatcher(splitedMsg[0], '^LUR$'):
		return splitedMsg[1]
	elif CMDMatcher(msgRecv, '^ERR\n$'):
		return 'ERR'
