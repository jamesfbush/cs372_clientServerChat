# Author:       James Bush
# Date:         2022-08-04
# Description:  Implementation of server-client chat per instructions.
# Sources:      https://docs.python.org/3/howto/sockets.html
#               https://realpython.com/python-sockets/
#               https://www.geeksforgeeks.org/python-convert-string-to-bytes/
#               https://www.geeksforgeeks.org/print-colors-python-terminal/


import server 


class MyClient(server.MySocket):
    """Class inherits all features of server.MySocket, initializing as a client.
    """
    def __init__(self, role='client', host='localhost',port=12000):
        super().__init__(role, host, port)
 
     
if __name__ == "__main__":

    # Start chat connection, set role 
    chatConnection = server.MySocket('client')
    correspondent = chatConnection.getCorrespondent()

    # Main chat loop -- will permit basic, turn-oriented chat
    while True:

        # Client enters message to send / sends
        msgSend = input("> ")
        chatConnection.sendMsg(msgSend)

        # If the message is /q to quit, close the socket and exit 
        if msgSend == '/q': 
            print("Exiting...")
            chatConnection.sock.close()
            break
    
        # Otherwise, receive messages from server and print to console
        msgRec = chatConnection.receiveMsg()
        if '/q' in msgRec:
            print("Exiting...")
            chatConnection.sock.close()
            break


        print(f"\n{correspondent}: {msgRec}\n")