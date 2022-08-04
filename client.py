import socket
import sys
import server 

# Create TCP/IP socket

class MyClient(server.MySocket):
    def __init__(self, role='client', host='localhost',port=12000):
        super().__init__(role, host, port)
     

    # *****************OLD MyCient********************
    # def __init__(self, sock=None):
    #     if sock is None:
    #         self.sock = socket.socket(
    #                         socket.AF_INET, socket.SOCK_STREAM)
    #     else:
    #         self.sock = sock
    #     self.MSGLEN = 4 # set msglength to 4, the length of the header

    # # Method set up connection with host        
    # def connect(self, host, port) :
    #     self.sock.connect((host, port))

    # # Method sends message and shows error if connect broke
    # def mysend(self, msg):
    #     totalsent = 0
    #     length = str((len(msg) + 4)).zfill(4) # pads with leading 0's
    #     msg = length + msg
    #     while totalsent < len(msg):
    #         sent = self.sock.send(msg[totalsent:].encode())
    #         if sent == 0:
    #             raise RuntimeError("socket connection broken")
    #         totalsent = totalsent + sent

    # # Method receives message, checks the length to receive correct amount
    # def myreceive(self):
    #     chunks = []
    #     newchunks = []
    #     bytes_recd = 0
    #     while bytes_recd < self.MSGLEN:
    #         chunk = self.sock.recv(min(self.MSGLEN - bytes_recd, 2048))
    #         if chunk == b'': # if received 0 bytes then connection broken
    #             raise RuntimeError("socket connection broken")
    #         chunks.append(chunk)
    #         bytes_recd = bytes_recd + len(chunk)
    #     length = int(b''.join(chunks))
    #     while bytes_recd < length:
    #         newchunk = self.sock.recv(min(length - bytes_recd, 2048))
    #         if newchunk == b'':
    #             raise RuntimeError("socket connection broken")
    #         newchunks.append(newchunk)
    #         bytes_recd = bytes_recd + len(newchunk)
    #     return b''.join(newchunks)
    # *****************OLD MyCient********************



# Begin Constructor 

# Starts the connection on the following host and port
# clientConnection = MyClient()
chatConnection = server.MySocket('client')
# clientConnection.connect('localhost', 12000)
print("Press any key to get started and connect to server")
while True:
    msgSend = input("> ")
    chatConnection.mysend(msgSend)
    if msgSend == '/q': # close the connection
        print("Exiting...")
        chatConnection.sock.close()
        break
    msgRec = chatConnection.myreceive()#.decode()
    print(msgRec)    