from socket import *
import threading
# 192.168.101.239 -- mac N
# alexpc 192.168.101.246 home

clients = []
users = []
chatArray =[]



serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to receive')



def recipient(senderName,chatName):
    for chat in chatArray:
        if chat[0] == chatName:
            if chat[1] == senderName:
                return chat[2]
            elif chat[2]== senderName:
                return chat[1]


def findAddress(destination_address):
    address =()
    for user in clients:
        
        if user[0] == destination_address:
            return user[1]

def findName(destination_address):
    address =()
    for user in clients:
        
        if user[1] == destination_address:
            return user[0]
def findChat(chatName):
    address =()
    for chat in chatArray:
        
        if chat[0] == chatName:
            return chat

        chatName = name[0]+name[1]

def findUserInfo(name):
    for client in clients:
        if name==client[0]:
            return client[1]
receiverAddress = ()
while True:
    # receives message with CODE PROTOCOL character at end of string
    # and formats to remove this character
    message, clientAddress = serverSocket.recvfrom(2048)
    decodedMessage = message.decode()

    messageArr = decodedMessage.split('\n')
    protocolCode=messageArr[0]

   
    if protocolCode == 'HELLO':

        if clientAddress not in clients:
            clients.append((messageArr[1], clientAddress))

    if protocolCode == 'NEW CHAT':
        person1 = findName(clientAddress)
        person2= messageArr[1]
        

        name = []
        name.append(person1)
        name.append(person2)
        name.sort()


        chatName = name[0]+name[1]
        #first item is chat name, secnd and third are the participants
        chat = []
        chat.append(chatName)
        chat.append(name[0])
        chat.append(name[1])

        chatArray.append(chat)

    if protocolCode == 'OLD CHAT':
        person1 = findName(clientAddress)
        person2= messageArr[1]

        name = []
        name.append(person1)
        name.append(person2)
        name.sort()

    if protocolCode=='CHAT':
        
        senderName = findName(clientAddress)
        sendTo = recipient(senderName, chatName)
        receiver_IP = findAddress(sendTo)
        serverSocket.sendto(messageArr[2].encode(), receiver_IP)


    
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

