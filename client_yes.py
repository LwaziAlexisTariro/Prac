from email import charset
from socket import *
import threading


serverName = '196.42.116.78'
userName = 'Alexis'
#should be IP address
serverPort = 12000
#Codes
initialConnection = "HELLO"
newChatCode = "NEW CHAT\n"
oldChatCode = "OLD CHAT\n"
chatCode = "CHAT\n"
leaveCode = "LEAVE\n"

clientSocket = socket(AF_INET, SOCK_DGRAM)
currentReceiver=''
def newChat():
    message= newChatCode+input("Who are you chatting to:\n")#includes code for brand new chat
    currentReceiver=message                                 #insert name
    clientSocket.sendto(message.encode(),(serverName,serverPort))

def oldChat():
    message= oldChatCode+input("Who are you chatting to:\n")#includes code for old chat
    #currentReceiver=message
    clientSocket.sendto(message.encode(),(serverName,serverPort))

message = input("Enter your username:\n")
tempmessage= initialConnection+'\n'+message
clientSocket.sendto(tempmessage.encode(), (serverName, serverPort))

def menu():
    menuInput = input("1 - Create new chat\n 2 - View chat\n")

menuInput = input("1 - Create new chat\n 2 - View chat\n")

if (menuInput == "1"):
    newChat()
else:
    oldChat()

    '''message= input("What is your message:\n")
    message+='_'+currentReceiver
    message+='_2'
    clientSocket.sendto(message.encode(),(serverName,serverPort))
    #modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    '''
def sending():                                                      
#takes and sends messages to server
   while True:
        message = input("Write message:\n")
                



        if (message == "LEAVE"):
            menu()
            clientSocket.sendto((leaveCode+message).encode(), (serverName, serverPort))
        else:
            clientSocket.sendto((chatCode+currentReceiver+'\n'+message).encode(), (serverName, serverPort))
     
        
def receiving():                                                    
#receives and prints messages from server
    while True:
         modifiedMessage, serverAddress =clientSocket.recvfrom(2048)    
        #errorcheck = checkHash(modifiedMessage.decode())
         print(modifiedMessage.decode())

sendthread = threading.Thread(target= sending)
receivethread = threading.Thread(target=receiving)                     

sendthread.start()
receivethread.start()

'''while True:
    #modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    #print(modifiedMessage.decode())
    message= input("What is your message")
    message+='2'
    clientSocket.sendto(message.encode(),(serverName,serverPort))''' 