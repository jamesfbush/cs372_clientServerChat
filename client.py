# Author:        James Bush
# Date:          2022-08-04
# Description:   Implementation of server-client chat per instructions.
# Sources:       https://docs.python.org/3/howto/sockets.html

import socket
import sys
import server 

# Create TCP/IP socket

class MyClient(server.MySocket):
    def __init__(self, role='client', host='localhost',port=12000):
        super().__init__(role, host, port)
 
     
if __name__ == "__main__":


    # Start chat connection, set role 
    chatConnection = server.MySocket('client')
    correspondent = chatConnection.getCorrespondent()
    # Main chat loop 
    while True:

        # Enter message to send / send it 
        msgSend = input("> ")
        chatConnection.sendMsg(msgSend)

        # If the message is /q to quit, close the socket and exit 
        if msgSend == '/q': 
            print("Exiting...")
            chatConnection.sock.close()
            break
    
        # Otherwise, receive messages from server and print to console
        msgRec = chatConnection.receiveMsg()

        #print(f"{correspondent}: {msgRec}")    

        print(f"\n{correspondent}: {msgRec}\n")