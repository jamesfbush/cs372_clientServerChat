# Author:       James Bush
# Date:         2022-08-02
# Description:  Implementation of project 4 per instructions. 
# Sources:      

from socket import *
import threading 

class Server:
    """"""

    def __init__(self, host, port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        # set option to reuse port immediately
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind((host, port)) # was '' in place of host
        # set to listen for TCP connections
        self.socket.listen(1)
        # set connection
        self.connection, self.addr = self.socket.accept()
        print("Chat running...")

    def recMessage(self):
        while True:
            request = self.connection.recv(1024)
            requestDecoded = request.decode()
            clientMessage = f"\nClient: {requestDecoded}"
            print(f"\033[34m {clientMessage}\033[00m")
            return 
         

    def sendMessage(self):
        ## old version

        while True: #This reprints the entry 
            print(">",end='')
            msg = input()#"\nServer: ")
            msg += "\n"
            # print("Server:",response)
            self.connection.send(msg.encode()) # Send response per instructions 
 


        # new version
        # totalsent = 0
        # length = str((len(msg) + 4)).zfill(4) # pads with leading 0's
        # msg = length + msg
        # while totalsent < len(msg):
        #     sent = self.socket.send(msg[totalsent:].encode())
        #     if sent == 0:
        #         raise RuntimeError("socket connection broken")
        #     totalsent = totalsent + sent
        
if __name__ == "__main__":
    myServer = Server('localhost',12000)

    # while True:

    backgroundSend = threading.Thread(target=myServer.sendMessage)
    backgroundSend.daemon = True 
    backgroundSend.start()
    
    # This works
    # clientMessage = myServer.recMessage()
    # if clientMessage:
    #     print(clientMessage)

    #Trying separate thread for receieve 
    backgroundRec = threading.Thread(target=myServer.recMessage())
    backgroundRec.daemon = True 
    backgroundRec.start()



        # send 

        # serverMessage = myServer.sendMessage()
        # if serverMessage:
        #     print(serverMessage)
    

