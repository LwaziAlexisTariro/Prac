import zlib
from socket import *
import threading

serverName = '196.168.101.229'

serverPort = 12000

#Protocol Codes
initialConnection = "HELLO\n"
newChatCode = "NEW CHAT\n"
oldChatCode = "OLD CHAT\n"
chatCode = "CHAT\n"
leaveCode = "LEAVE\n"

clientSocket = socket(AF_INET, SOCK_DGRAM)
currentReceiver=''#################!!!!!!!!!!!! should be deleted? referenced later but stays empty

def newChat():                                                      #function for when user wants to start a new chat
    message= newChatCode+input("Who are you chatting to:\n")        #includes code for brand new chat
    clientSocket.sendto(message.encode(),(serverName,serverPort))   #sends message to server

def oldChat():                                                      #function for when user wants to open an old chat         
    message= oldChatCode+input("Who are you chatting to:\n")        #includes code for old chat
    clientSocket.sendto(message.encode(),(serverName,serverPort))

def menu():                                                         #menu displayed to user to select chat type
    menuInput = input("1 - Create new chat\n 2 - View chat\n")
    if (menuInput == "1"):
        newChat()
    else:
        oldChat()

def checkHash(message, hashValue):
    tempMessage='b'+message#function for checking hash value matches hashed message
    if str(zlib.adler32(message.encode()))==hashValue:
        return True
    else: 
        return False

message = input("Enter your username:\n")                           #user enters username
tempmessage= initialConnection+message                              #client sends first message to server, indicating that it is "online"
clientSocket.sendto(tempmessage.encode(), (serverName, serverPort))

menuInput = input("1 - Create new chat\n 2 - View chat\n")          #menu displayed to user to select chat type

if (menuInput == "1"):
    newChat()
else:
    oldChat()

def sending():                                                      #function that is turned into thread and sends messages to the server
   while True:
        message = input()
                
        if (message == "LEAVE"):                                    #initiates leave protocol
                                                            #user given menu again to select a new chat
            clientSocket.sendto((leaveCode+message).encode(), (serverName, serverPort))
            menu()  
        else:
            hashM='"'+message+'"'
            clientSocket.sendto((chatCode+currentReceiver+'\n'+message+'\n'+str(zlib.adler32(message.encode()))).encode(), (serverName, serverPort))
           #clientSocket.sendto((chatCode+currentReceiver+'\n'+message).encode(), (serverName, serverPort))  
        
def receiving():                                                    #function that is turned into thread and receives messages from the server
    while True:
        modifiedMessage, serverAddress =clientSocket.recvfrom(2048)
        decodedMessage=modifiedMessage.decode()
        newLine='\n'
        if newLine in decodedMessage:
            
            messageArr = decodedMessage.split('\n')           #splits 2 line message, first line with actual message, second with the hash value for comparison later
            actMessage = messageArr[0].replace('\t','')
           
           
            
            #removes tabbing in front of message, in order to compare with the right hash function
            errorcheck = checkHash(actMessage, messageArr[1])           #error detection

            print(messageArr[0])                                        #prints chat message

            if (errorcheck == False):                                   #if the hash check returns false, the message is corrupt and the user is notified
                print("Please note that this message might be corrupted.")
        else:
            print(decodedMessage)
        
#chat header
print('------------------------------Joined chat------------------------------')
print('-------------Enter LEAVE to leave chat and start a new one-------------')
print('-----------------------------------------------------------------------')

#sending and receiving threads are created and started
sendthread = threading.Thread(target= sending)
receivethread = threading.Thread(target=receiving)                     

sendthread.start()
receivethread.start()