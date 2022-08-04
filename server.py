
from socket import *
import random

class MySocket:

    def __init__(self, role=None, host='localhost',port=12000):
        self.MSGLEN = 4
        if role == 'server':
            self.role = role
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            ## TRYING THIS
            self.sock.bind((host, port)) # was '' in place of host
            # set to listen for TCP connections
            self.sock.listen(1)
            # set connection
            self.clientConnection, self.addr = self.sock.accept()
            print("Chat running...")            
            ## -----------
        elif role == 'client':
            self.role = role
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect((host, port))
            self.clientConnection = self.sock # the connection is itself 

    # TODO refactor 
    # Method sends message and adds a header indicating length of msg
    def mysend(self, msg):
        totalsent = 0
        length = str((len(msg) + 4)).zfill(4) # pads with leading 0's
        msg = length + msg
        while totalsent < len(msg):
            sent = self.clientConnection.send(msg[totalsent:].encode())
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    # TODO refactor
    # Method receives message, checks the length to receive correct amount
    def myreceive(self):
        chunks = []
        newchunks = []
        bytes_recd = 0
        while bytes_recd < self.MSGLEN:
            chunk = self.clientConnection.recv(min(self.MSGLEN - bytes_recd, 2048))
            if chunk == b'': # if received 0 bytes then connection broken
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        length = int(b''.join(chunks))
        while bytes_recd < length:
            newchunk = self.clientConnection.recv(min(length - bytes_recd, 2048))
            if newchunk == b'':
                raise RuntimeError("socket connection broken")
            newchunks.append(newchunk)
            bytes_recd = bytes_recd + len(newchunk)
        #correspondent = [i for i in ['server','client'] if i != self.role][0].capitalize()
        # message = self.strColor(f"{b''.join(newchunks).decode()}\n", 'blue')
        # return message
        return b''.join(newchunks).decode()

    def strColor(self,string,color):
        colors = {  
            'blue':str(34),
            'red':str(91)
        }
        return f"\033[{colors[color]}m{string}\033[00m"

    def networkingTriviaQA(self):
        
        questionAnsBank = [ 
            ['TCP is a connection-oriented service [T/F]\n',['true','t']],
            ['UDP is a \"fire and forget\" type of service [T/F]:\n',['true','t']],
            ['Mobile phone operate at network core [T/F]\n',['false','f']]        
        ]
        return questionAnsBank[random.randint(0, len(questionAnsBank)-1)]

    def networkingTrivia(self):
        welcome = f"{'*'*30}\nWelcome to networking trivia"
        score = 0
        questions = 0 
        # qAndA = {   'TCP is a connection-oriented service [T/F]':['true','t'],
        #             'UDP is a \"fire and forget\" type of service [T/F]:':['true','t']}
        
        qAndA = self.networkingTriviaQA()
        # need support or asked questions

        while True:
            qAndA = self.networkingTriviaQA()
            question = qAndA[0]
            answers = qAndA[1]
            print(question) # send message
            self.mysend(f"{welcome}\n\n{question}")
            #answer = input("Answer: ").lower() # take response 
            answer = self.myreceive()
            print("PARSED ANS",len(answer),answer)
            if answer == "\stop":
                break
            elif answer in answers:
                score += 1
                questions += 1
                print("Correct!") # send message
                self.mysend("Correct")
            else:
                questions += 1
                message = f"incorrect. acceptable answers are {[str(i) for i in answers]}"
                print(self.strColor(message,'red')) # send message
                self.mysend(message)
        message = f"Score: {(score/questions)*100}%"
        print(message) # send message 
        self.mysend(message)

if __name__ == "__main__":
    # Initiate chat session
    chatConnection = MySocket('server')


    # Loop will permit basic back-and-forth chat
    while True:
            correspondent = [i for i in ['server','client'] if i != chatConnection.role][0].capitalize()
            message = chatConnection.myreceive()#.decode()
            # if (message == '/q'): #close connection if /q
            if '/q' in message:
                print("Exiting...")
                chatConnection.sock.close()
                break
                # needs to quit the session/close down whatever
            if '\game' in message:
                chatConnection.networkingTrivia()
            print(f"\n{correspondent}: {message}")
            reply = input("> ")
            chatConnection.mysend(reply)
            # if (message == 'quit'): #close connection if /q
            #     break
            #clientConnection.mysend(result) 
            

