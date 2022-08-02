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
        self.socket.bind(('', port))
        # set to listen for TCP connections
        self.socket.listen(1)
        # set connection
        self.connection, self.addr = self.socket.accept()
        print("Chat running...")

    def recMessage(self):
        request = self.connection.recv(1024)
        requestDecoded = request.decode()
        clientMessage = f"\nClient: {requestDecoded}"
        print(clientMessage)
        return 

    def sendMessage(self):
        # while True: This reprints the entry 
            response = input("\nServer: ")
            response += "\n"
            # print("Server:",response)
            self.connection.send(response.encode()) # Send response per instructions 
            
if __name__ == "__main__":
    myServer = Server('localhost',12000)



    
    while True:

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
    

