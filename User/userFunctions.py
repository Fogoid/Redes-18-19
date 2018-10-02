def LSDCommand(mySocket, size):
	
	message = "LSD"
	mySocket.send(message.encode())
	message = mySocket.recv(size)
	message = message.decode()
	print(message[4:])
