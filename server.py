# Author:       James Bush
# Date:         2022-08-04
# Description:  Implementation of server-client chat per instructions.
# Sources:      https://docs.python.org/3/howto/sockets.html
#               https://realpython.com/python-sockets/
#               https://www.geeksforgeeks.org/python-convert-string-to-bytes/
#               https://www.geeksforgeeks.org/print-colors-python-terminal/ 


from socket import *
import random

class MySocket:
    """Class establishes chat connection depending on passed role, i.e.,
    ('client'/'server').
    """

    def __init__(self, role=None, host='localhost',port=12000):

        self.MSGLEN = 4

        if role == 'server':
            self.role = role
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # reuse port
            self.sock.bind((host, port))
            self.sock.listen(1) # 1? 5? 
            self.clientConnection, self.addr = self.sock.accept()
  
        elif role == 'client':
            self.role = role
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect((host, port))
            self.clientConnection = self.sock # the connection is itself 
        
        self.welcome(self.role)


    def sendMsg(self, msg):
        """Send string with header indicating length of string.
        """
        totalsent = 0
        msg = f"{str((len(msg) + 4)).zfill(4)}{msg}"
        while totalsent < len(msg):
            sent = self.clientConnection.send(msg[totalsent:].encode())
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent += sent

    def receiveMsg(self):
        """Receive string message by chunks. Error if connection broken."""
        chunks = []
        newChunks = []
        bytesRecd = 0
        while bytesRecd < self.MSGLEN:
            chunk = self.clientConnection.recv(min(self.MSGLEN - bytesRecd, 2048))
            # connection broken
            if chunk == b'': 
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytesRecd += len(chunk)
        length = int(b''.join(chunks))
        while bytesRecd < length:
            newchunk = self.clientConnection.recv(min(length - bytesRecd, 2048))
            # connection broken
            if newchunk == b'':
                raise RuntimeError("socket connection broken")
            newChunks.append(newchunk)
            bytesRecd += len(newchunk)

        # return message
        return b''.join(newChunks).decode()

    def welcome(self, role):
        print(f"{'='*40}\nConnected to chat!\nType '/q' to quit/exit.\n{'='*40}")
        if role == 'server':
            print("Waiting on message from client...\n")
        else:
            print("Your turn to send message to server.\n")

    def getCorrespondent(self):
        """Return correspondent entity name."""
        return [i for i in ['server','client'] if i != self.role][0].capitalize()

    def strColor(self,string,color):
        """Take string, make it colorful."""
        colors = {  
            'blue':str(34),
            'red':str(91),
            'green':str(92),
            'cyan':str(96)
        }
        return f"\033[{colors[color]}m{string}\033[00m"

    def networkingTriviaQA(self):
        """When called, return random question and possible answers from bank."""

        questionAnsBank = [ 
            ['TCP is a connection-oriented service [T/F]\n',['true','t']],
            ['UDP is a \"fire and forget\" type of service [T/F]:\n',['true','t']],
            ['Mobile phones operate at network core [T/F]\n',['false','f']],
            ['At the transport layer, what is the payload?\
                \n\n1. application data\n2. transport data',['1','application data']],
            ['In the Internet protocol stack, the Application Layer is responsible for assembling user data to be sent [T/F]',['true','t']],
            ['If I were to send information into the internet with your IP address listed as the sender IP, I would be:\
                \n\n1. executing DDoS\n2. spoofing',['2','spoof','spoofing']],
            [' A paired IP address and port number is called a:\n\n1. router\n2. socket',['2','socket']],
            ['In a ______ architecture, one host is always on, and other hosts may connect\
                and be continually serviced by this first host.\
                    \n1. hybrid\n2. client-server\n3. peer-to-peer',['2', 'client-server']]      
        ]
        return questionAnsBank[random.randint(0, len(questionAnsBank)-1)]

    def networkingTrivia(self):
        """ Ask questions from bank, sending question through chat. 
        Take answers through chat, check against model answers, provide feedback. 
        When receive /stop, stop game and send score. 
        """
        welcome = self.strColor(f"\n{'*'*40}\nWelcome to Network Trivia!\n{'*'*40}\n",'cyan')
        score = 0
        questions = 0 

        # main play loop
        while True:
            qAndA = self.networkingTriviaQA()
            question = qAndA[0]
            answers = qAndA[1]
            print(question) # see question server-side

            # welcome greeting / ask question 
            if questions == 0: 
                self.sendMsg(f"{welcome}\nQuestion {questions+1}: {question}")
            else: 
                self.sendMsg(f"\nQuestion {questions+1}: {question}")

            # obtain and parse answer 
            answer = self.receiveMsg().lower()

            # stop if requested 
            if answer == "/stop":
                break

            # still honor request to quit chat with /q
            if answer == "/q":
                print("Exiting...")
                chatConnection.sock.close()
                exit()

            # check substantive answer, generate appropriate feedback 
            elif answer in answers:
                score += 1
                questions += 1
                feedback = self.strColor('Correct!', 'green')
            else:
                questions += 1
                feedback = self.strColor(f"Incorrect. Acceptable answers are {[str(i) for i in answers]}",'red')

            # send feedback on answer
            message = f"{feedback}\n\nHit Enter/Return for next question or '/stop' to quit and see score.\n"
            self.sendMsg(message)

            # get response, whether to continue or get score and quit
            response = self.receiveMsg().lower()
            print(response)
            if response == "/stop":
                break
            
        # send score and return to main program 
        if questions > 0:
            score = round((score/questions),3)*100
        elif questions == 0:
            score = 0
        message = f"\n{'*'*40}\nQuestions: {questions} Score: {score}%\nThanks for playing Network Trivia!\n{'*'*40}\n"
        print(message) 
        self.sendMsg(message)
        return

if __name__ == "__main__":
    # Initiate chat session
    chatConnection = MySocket('server')
    correspondent = chatConnection.getCorrespondent()

    # Main chat loop -- will permit basic, turn-oriented chat
    while True:

            # Server waits on message from client
            msgRec = chatConnection.receiveMsg()

            # Close connection if /q in message from client
            if '/q' in msgRec:
                print("Exiting...")
                chatConnection.sock.close()
                break

            # EXTRA CREDIT - start game if /game in message
            if '/game' in msgRec:
                chatConnection.networkingTrivia()

            # Normal message send
            else:
                print(f"\n{correspondent}: {msgRec}\n")
                msgSend = input("> ")

                chatConnection.sendMsg(msgSend)

                if '/q' in msgSend:
                    print("Exiting...")
                    chatConnection.sock.close()
                    break
