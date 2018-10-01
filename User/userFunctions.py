def LSDCommand():
	message = "LSD"
	mySocket.send(message.encode())

	message = mySocket.recv(buffersize)
	message = message.decode()
	print(message[4:])
