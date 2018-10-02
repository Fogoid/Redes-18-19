#This file describes the routines that are responsible for sending specific protocol
#syntax to the CS, describing the User - CS protocol on the user side.

def LSDCommand(mySocket, size):
	
	messageSent = "LSD\n"
	mySocket.send(messageSent.encode())

	messageRecv = mySocket.recv(size)
	messageRecv = messageRecv.decode()

	print(messageRecv[4:])

	return 1

#The command that processes the Delete user request
def DLUCommand():
		messageSent = 'DLU\n'
		mySocket.send(messageSent.encode())

		messageRecv = mySocket.recv(buffersize)
		messageRecv = messageRecv.decode()

		if messageRecv[0: len("DLR ")] == "DLR ":
			print(messageRecv[len("DLR "):], end="")
			if messageRecv[len("DLR "):] == "OK":
				print(messageRecv[len("DLR "):])
				return 0;
		return 1;