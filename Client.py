import socket

serverName = 'localhost'
serverPort = 12345
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    word = input('Input a word: ')
    print("Sending word:", word)
    clientSocket.send(word.encode())
    if word == '@':
        break
    synonym = clientSocket.recv(1024).decode()
    print("Received synonym:", synonym)
   

clientSocket.close()

