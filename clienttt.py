from email import charset
from socket import *
import threading


serverName = '196.42.95.187'
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
    #currentReceiver=message                                 #insert name
    clientSocket.sendto(message.encode(),(serverName,serverPort))

def oldChat():
    message= oldChatCode+input("Who are you chatting to:\n")#includes code for old chat
    #currentReceiver=message
    clientSocket.sendto(message.encode(),(serverName,serverPort))


def menu():
    menuInput = input("1 - Create new chat\n 2 - View chat\n")
    if (menuInput == "1"):
        newChat()
    else:
        oldChat()

message = input("Enter your username:\n")
tempmessage= initialConnection+'\n'+message
clientSocket.sendto(tempmessage.encode(), (serverName, serverPort))

menuInput = input("1 - Create new chat\n 2 - View chat\n")

if (menuInput == "1"):
    newChat()
else:
    oldChat()

def checkHash(message, hashValue):
    if hash(message)== hashValue:
        return True
    else: 
        return False


def sending():                                                      
#takes and sends messages to server
   while True:
        message = input()
                



        if (message == "LEAVE"):
            menu()
            clientSocket.sendto((leaveCode+message).encode(), (serverName, serverPort))
        else:
           clientSocket.sendto((chatCode+currentReceiver+'\n'+message).encode(), (serverName, serverPort))

           # clientSocket.sendto((chatCode+currentReceiver+'\n'+message+'\n'+hash(message)).encode(), (serverName, serverPort))
     
        
def receiving():                                                    
#receives and prints messages from server
    while True:
        modifiedMessage, serverAddress =clientSocket.recvfrom(2048)    
        messageArr = modifiedMessage.decode().split('\n')
        errorcheck = checkHash(messageArr[0], messageArr[1])#error detection
        #print(modifiedMessage.decode())
        print(messageArr[0])

        if (errorcheck == False):
            print("Please note that this message might be corrupted.")

print('Joined chat')
print('----------------------------------')

sendthread = threading.Thread(target= sending)
receivethread = threading.Thread(target=receiving)                     

sendthread.start()
receivethread.start()