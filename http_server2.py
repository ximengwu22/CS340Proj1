from socket import *
from os import path
import select
import queue as Q


def main():
    # create TCP socket
    serverPort = 8880
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setblocking(0) # set socket as non-block

    # bind socket and listen
    try:
        serverSocket.bind(("", serverPort))
        serverSocket.listen(10)
    except error:
        print(error)

    # initialize open connection input list
    inputs = [serverSocket]

    # initialize response sending output list
    outputs = []

    msg = {}

    while inputs:
        print('-waiting for the next event')

        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        for s in readable:
            print("Enter readable layer, s: ", s)
            print("\t readable: ", readable)

            if s is serverSocket:
                connSocket, addr = s.accept() # connSocket: NEW CONNECTION SOCKET
                print("-    connection from:",addr)
                connSocket.setblocking(0) # set unblock
                inputs.append(connSocket)
                #connSocket.settimeout(10)
                msg[connSocket] = Q.Queue()
            else:
                data = s.recv(1024).decode()
                if data:
                    print("-    received ",data)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    print("-    closing ", addr)
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del msg[s]


        for ss in writable:
            try:
                next_msg = msg[ss].get_nowait()

            except Q.Empty:
                print('  ', ss.getpeername(), 'queue empty')
                outputs.remove(ss)
            else:
                print('-    sending "%s" to %s' % \
                      (next_msg, ss.getpeername()))
                ss.send(next_msg)

        for s in exceptional:
            for s in exceptional:
                print('- exception condition on', s.getpeername())
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                del msg[s]


if __name__ in '__main__':
    main()
