from socket import *
from os import path

def main():
    # create TCP socket
    serverPort = 8888
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # bind socket and listen
    try:
        serverSocket.bind(("", serverPort))
        serverSocket.listen(1)
    except error:
        print(error)

    # initial open connection list
    openConn = []

    while True:
        connSocket, addr = serverSocket.accept() # connSocket: NEW CONNECTION SOCKET
        #connSocket.settimeout(10)

        respBuf = connSocket.recv(1024).decode()

        print("-response::", respBuf)




        connSocket.close()

if __name__ in '__main__':
    main()
