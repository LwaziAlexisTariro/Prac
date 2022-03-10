from socket import *

import threading
# 192.168.101.239 -- mac N
# alexpc 192.168.101.246 home

clients = []                                            #stores clients' information         
chatArray=[]                                            #stores chats, clients/users involved, messages and online status
#chatArray =['','','',[[]],[]]

ossDetectionA = False
lossDetectionB = False

serverPort = 12000                                      #server port
serverSocket = socket(AF_INET, SOCK_DGRAM)              #server socket
serverSocket.bind(('', serverPort))                     #binds server port to socket
print('The server is ready to receive')


def sendMessage(message, receiver_IP):                  #function for sending messages to receiver client
    serverSocket.sendto(message.encode(), receiver_IP)


def recipient(senderName,chatName):                     #finds recipient's name based off of the chat they are part of and the sender
    for chat in chatArray:
        if chat[0] == chatName:
            if chat[1] == senderName:
                return chat[2]
            elif chat[2]== senderName:
                return chat[1]


def findAddress(username):                   #finds client's ip address based off of their username
    for user in clients:
        
        if user[0] == username:
            return user[1]

def findName(destination_address):           #finds client's username based off of their ip address and socket
    for user in clients:
        
        if user[1] == destination_address:
            return user[0]

def findChat(chatName):                     #finds chat with the chatname
    for chat in chatArray:
        
        if chat[0] == chatName:
            return chat

        #chatName = clientNames[0]+clientNames[1]

def storeMessage(sender, receiver, message):    #stores chat messages for history functionality
    for chat in chatArray:
        
        if chat[0] == chatName:     
            chat[3].append([sender,receiver, message, False])
    
    
receiverAddress = ()
while True:
    # receives message with CODE PROTOCOL character at end of string
    # and formats to remove this character
    message, clientAddress = serverSocket.recvfrom(2048)
    
    decodedMessage = message.decode()
   
        

    messageArr = decodedMessage.split('\n')
    protocolCode=messageArr[0]
    #checkMessage1 = messageArr[2]

    
   
    if protocolCode == 'HELLO':
        tempClient=(messageArr[1], clientAddress)
        if tempClient not in clients:                        #checks if client is in address list, if not, they are added
            clients.append((messageArr[1], clientAddress))

    if protocolCode == 'NEW CHAT':
        person1 = findName(clientAddress)                       #stores message sender
        person2= messageArr[1]                                  #stores message receiver
        

        clientNames = [person1, person2]
        #name.append(person1)
        #name.append(person2)
        clientNames.sort()                                      #sorts names in alphabetical order (for identification purposes, alphabetic orde to reduce dplication o)


        chatName = clientNames[0]+clientNames[1]                #creates chat identifier
        
        #first item is chat name, secnd and third are the participants
        chat = []

        activeUsers = [clientNames[0], clientNames[1]]          #active/online users
        chat.append(chatName)                                   #populating new chat entry
        chat.append(clientNames[0])
        chat.append(clientNames[1])
        #activeUsers.append(name[0])
        #activeUsers.append(name[1])
       
        chat.append([])
        chat.append(activeUsers)



        if chat not in chatArray:
            chatArray.append(chat)
        else:
            for chat in chatArray:

                if chatName== chat[0]:


                    for message in chat[3]:
                        if message[3]==False:
                            receiver_IP = findAddress(message[1])

                            if message[1] in chat[4]:
                                sendMessage(message[2], receiver_IP)
                                message[3]=True
                                sendMessage("**Message sent**", clientAddress)

                                
    if protocolCode == 'OLD CHAT':
        person1 = findName(clientAddress)                       #stores message sender
        person2= messageArr[1]                                  #stores message receiver
        

        clientNames = [person1, person2]
        #name.append(person1)
        #name.append(person2)
        clientNames.sort()                                      #sorts names in alphabetical order (for identification purposes, alphabetic orde to reduce dplication o)


        chatName = clientNames[0]+clientNames[1]                #creates chat identifier
        
        #first item is chat name, secnd and third are the participants
      #active/online users
       
        #activeUsers.append(name[0])
        #activeUsers.append(name[1])
       
    
                
        
        for chat in chatArray:

            if chatName== chat[0]:
                chat[4].append(person1)
                flag=False
             
                sendMessage('---------------------This is the beginning of your chat---------------',receiver_IP)
                for message in chat[3]:
                    if(message[3]==True):
                        if(message[1]==person2):
                            sendMessage(message[2], receiver_IP)
                        else:
                            sendMessage('\t\t\t\t\t\t\t'+message[2], receiver_IP)
                    elif(message[3]==False and flag==False ):
                        sendMessage('*************************   Unread Messages    ***********************',receiver_IP)
                        sendMessage('\t\t\t\t\t\t\t'+message[2], receiver_IP)
                        tempClientAddress= findAddress(message[0])
                        sendMessage("**Message sent**", tempClientAddress)
                        message[3]=True
                        flag=True
                    else:
                        sendMessage('\t\t\t\t\t\t\t'+message[2], receiver_IP)
                        message[3]=True


    if protocolCode=='CHAT':

        sendMessage("**Message received by server**", clientAddress)
        
        senderName = findName(clientAddress)
        sendTo = recipient(senderName, chatName)
        receiver_IP = findAddress(sendTo)
    
        
        storeMessage(senderName,sendTo,messageArr[2])
        for chat in chatArray:

                if chatName== chat[0]:


                    for message in chat[3]:
                        if message[3]==False:
                            receiver_IP = findAddress(message[1])

                            if message[1] in chat[4]:
                                sendMessage('\t\t\t\t\t\t\t'+message[2]+'\n'+messageArr[3], receiver_IP)
                                message[3]=True
                                sendMessage("**Message sent**", clientAddress)

        #sendMessage('\t\t\t'+messageArr,receiver_IP)
        
        
    if protocolCode=='LEAVE':
        clientName = findName(clientAddress)

        for chat in chatArray:
            if chatName== chat[0]:
                chat[4].remove(clientName)
            
        



    
        #first item is chat name, secnd and third are the participants
     


        # CHECK FOR RECEIVER ADDRESS IN CLIENT ADDRESS TABLE. IF MATCH, SET RECEIVER IP AND PORT
   
        '''EACH MESSAGE CARRIES THE IP ADDRESS OF THE INTENDED RECEPIENT WITH IT. 
        CURRENT FORMAT:
        MESSAGE_IP_2'''
        # THIS CODE ENABLES THE RECEIVER CLIENT TO CHANGE
        # CODE LOOKS FOR RECEIVER IP MATCH IN CLIENT ADDRESS TABLE AND SETS RECEIVER ADDRESS TO THIS NEW MATCH
    


"""while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    decodedMessage= message.decode()
    if decodedMessage[-1]=='0':
        if clientAddress not in clients:
            clients.append(clientAddress)
    if decodedMessage[-1]=='1':
        for client in clients:
            tempmessage= message[:-1]
            if client[0]==tempmessage:
                receiverAddress=client
    if decodedMessage[-1]=='2':
        serverSocket.sendto(message.encode(), receiverAddress)
    
"""
#modifiedMessage = message.decode().upper()
#serverSocket.sendto(modifiedMessage.encode(), ip(''))
#serverSocket.sendto(modifiedMessage.encode(), clientAddress)


'''def sendAll():
    for client in clients:
        modifiedMessage = message.decode()
        serverSocket.sendto(modifiedMessage.encode(), client)'''

