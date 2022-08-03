# Author:       James Bush
# Date:         2022-08-02
# Description:  Implementation of project 4 per instructions. 
# Sources:      

from socket import *
import threading 
import time as tm
import random 
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


    def recMessage(self, internal=False):
        while True:
            request = self.connection.recv(1024)
            requestDecoded = request.decode()
            #print(requestDecoded)
            if requestDecoded[:2] == '\q':
                exit()
            if requestDecoded[:5] == '\game':
                self.networkingTrivia()
            clientMessage = f"\nClient: {requestDecoded}"
            print(f"\033[34m {clientMessage}\033[00m")
            if internal:
                return requestDecoded
         

    def sendMessage(self,msg=None):
        ## old version
        if msg:
            msg += "\n"
            self.connection.send(msg.encode()) # Send response per instructions 
            return
        else:
            while True: #This reprints the entry 
                msg = input()#"\nServer: ")
                msg += "\n"
                self.connection.send(msg.encode()) # Send response per instructions 
 

    def networkingTriviaQA(self):
        

        questionAnsBank = [ ['TCP is a connection-oriented service [T/F]',['true','t']],
                            ['UDP is a \"fire and forget\" type of service [T/F]:',['true','t']],
                            ['Mobile phone operate at network core [T/F]',['false','f']]        
        ]
        index = random.randint(0, len(questionAnsBank)-1)
        print("INDEX",index)
        return questionAnsBank[index]

    def networkingTrivia(self):
        self.sendMessage("Welcome to networking trivia")
        score = 0
        questions = 0 
        rounds = 5
        # qAndA = {   'TCP is a connection-oriented service [T/F]':['true','t'],
        #             'UDP is a \"fire and forget\" type of service [T/F]:':['true','t']}
        
        qAndA = self.networkingTriviaQA()

        for i in range(rounds):
            qAndA = self.networkingTriviaQA()
            question = qAndA[0]
            answers = qAndA[1]
            print(question) # send message
            self.sendMessage(question)
            #answer = input("Answer: ").lower() # take response 
            answer = self.recMessage(True)
            answer = answer[:answer.find("\r")].lower()
            if answer in answers:
                score += 1
                questions += 1
                print("Correct!") # send message
                self.sendMessage("Correct")
            else:
                questions += 1
                message = f"incorrect. acceptable answers are {[str(i) for i in answers]}"
                print(message) # send message
                self.sendMessage(message)
        message = f"Score: {(score/questions)*100}%"
        print(message) # send message 
        self.sendMessage(message)
        return 

        
        
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



