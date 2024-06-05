import socket 
import threading

DICTIONARY_FILE = 'synonym.txt'

class ServeClient(threading.Thread): 
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        while True:
            data = self.conn.recv(1024).decode()
            if data == '@':
                break
            print("Received word:", data)
            if data in engDict:
                synonym = engDict[data]
                print("Sending synonym:", synonym)
                self.conn.send((data + ' ==> ' + synonym).encode())
                
            else:
                self.conn.send(('No synonym found'+ data).encode())

        self.conn.close()

engDict = {}
with open(DICTIONARY_FILE) as f:
    for line in f:
        tok = line.split()
        engDict[tok[0]] = tok[1]

serverName = 'localhost'
serverPort = 12345
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)
print('Server ready to receive')

threads = []
while True:
    connectionSocket, addr = serverSocket.accept()
    newThread = ServeClient(connectionSocket, addr)
    newThread.start()
    threads.append(newThread)

for t in threads:
    t.join()
