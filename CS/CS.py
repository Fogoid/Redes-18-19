#! /usr/bin/python3
import sys
import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind(('localhost', 80))

serverSocket.listen(5)

(clientSocket, address) = serverSocket.accept()

while True:
	message = clientSocket.recv(230)
	print(message.decode())	
	clientSocket.send(input().encode())