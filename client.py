from ast import While
from socket import * 

serverName = "196.42.95.187"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input("Enter your username:   ")

clientSocket.sendto(message.encode(), (serverName, serverPort))

#message = input("Who are you chatting to?:  ")
#clientSocket.sendto(message.encode(), (serverName, serverPort))

#modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

while True:
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
    message = input("Write message:     ")
    clientSocket.sendto(message.encode(), (serverName, serverPort))
