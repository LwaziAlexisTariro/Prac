from socket import *

import threading
# 192.168.101.239 -- mac N
# alexpc 192.168.101.246 home

clients = []                                            #stores clients' information         
chatArray=[]                                            #stores chats, clients/users involved, messages and online status

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


    
   
    if protocolCode == 'HELLO':
        tempClient=(messageArr[1], clientAddress)
        if tempClient not in clients:                        #checks if client is in address list, if not, they are added
            clients.append((messageArr[1], clientAddress))

    if protocolCode == 'NEW CHAT':
        person1 = findName(clientAddress)                       #stores message sender
        person2= messageArr[1]                                  #stores message receiver
        

        clientNames = [person1, person2]
        clientNames.sort()                                      #sorts names in alphabetical order (for identification purposes, alphabetic orde to reduce dplication o)


        chatName = clientNames[0]+clientNames[1]                #creates chat identifier
        
        #first item is chat name, secnd and third are the participants
        chat = []

        activeUsers = [clientNames[0], clientNames[1]]          #active/online users
        chat.append(chatName)                                   #populating new chat entry
        chat.append(clientNames[0])
        chat.append(clientNames[1])
       
        chat.append([])
        chat.append(activeUsers)


        
        if chat not in chatArray:                               #if chat not already in array, add it
            chatArray.append(chat)
        else:
            for chat in chatArray:

                if chatName== chat[0]:

                    #IF ANY MESSAGES IN CHAT HAVE NOT BEEN SENT, AND RECEIVER IS NOW ONLINE,
                    #  DELIVER THE MESSAGES TO RECEIVER
                    # AND NOTIFY SENDER THAT MESSAGES HAVE BEEN DELIVERED
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
        clientNames.sort()                                      #sorts names in alphabetical order (for identification purposes, alphabetic orde to reduce dplication o)


        chatName = clientNames[0]+clientNames[1]                #creates chat identifier
        
        #first item is chat name, secnd and third are the participants
      #active/online users
        for chat in chatArray:
            #add user to list of users currently online in chat
            if chatName== chat[0]:
                chat[4].append(person1)
                flag=False
             
                sendMessage('---------------------This is the beginning of your chat---------------',receiver_IP)
                #send Chat history of all messages from beginning of chat
                for message in chat[3]:
                    #resends all messsages that have already been delivered
                    if(message[3]==True):
                        if(message[1]==person2):
                            sendMessage(message[2], receiver_IP)
                        else:
                            sendMessage('\t\t\t\t\t\t\t'+message[2], receiver_IP)

                    #sends the rest of messages that havent yet been delivered under the heading Unread messages
                    #also takes into account the sender and receiver of each message and formats messages accordingly
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
        #notify the sender client that the message has been received by the server
        sendMessage("**Message received by server**", clientAddress)
        
        senderName = findName(clientAddress)
        sendTo = recipient(senderName, chatName)
        receiver_IP = findAddress(sendTo)
    
        #adds the message to the list of messages in chat
        storeMessage(senderName,sendTo,messageArr[2])
        for chat in chatArray:

                if chatName== chat[0]:

                    #loops through messages and, if the receiver is online, sends any messages to the receiver that have not already been sent.
                    for message in chat[3]:
                        if message[3]==False:
                            receiver_IP = findAddress(message[1])

                            if message[1] in chat[4]:
                                sendMessage('\t\t\t\t\t\t\t'+message[2]+'\n'+messageArr[3], receiver_IP)
                                message[3]=True
                                sendMessage("**Message sent**", clientAddress)

    #if the protocol code is leave, removes user from the chat's list of currently active users
    if protocolCode=='LEAVE':
        clientName = findName(clientAddress)

        for chat in chatArray:
            if chatName== chat[0]:
                chat[4].remove(clientName)


