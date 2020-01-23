from socket import *
from os import path
import re
import sys
import queue
import select


def checkFileExist(fname):
    # print("Exist or Not:", path.exists(fname))

    return path.exists(fname)


def constructMsg(s, body, fileName):
    header = '''HTTP/1.1 %s\r\nContent-Type: text/html\r\n\r\n''' % s
    header += body
    if checkFileExist(fileName) and checkEndWith(fileName):
        f = open(fileName, 'r')
        header += f.read()
        f.close()
    return header.encode()


def checkEndWith(s):
    return ".html" in s or ".htm" in s


def getAction(fname):
    get_pattern_1 = re.compile('GET\s/(.*?)\s')
    get_action = ''
    if len(re.findall(get_pattern_1, fname)) > 0:
        get_action = re.findall(get_pattern_1, fname)[0]
    return get_action


def main(p):
    serverPort = p
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setblocking(0)
    try:
        serverSocket.bind(("", serverPort))
        serverSocket.listen(5)


    except error:
        print(error)
    inputs = [serverSocket]
    outputs = []

    while inputs:

        read, write, err = select.select(inputs, outputs, inputs)
        for r in read:
            if r is serverSocket:
                connSocket, addr = r.accept()
                print('connection from:', connSocket, addr)
                connSocket.setblocking(0)
                inputs.append(connSocket)

            else:
                data = r.recv(1024).decode()

                if data:
                    respBuf = data
                    get_content = getAction(respBuf)

                    if checkFileExist(get_content):
                        if checkEndWith(get_content):
                            corrMsg = constructMsg("200 OK", '', get_content)
                            r.send(corrMsg)
                        else:
                            errBd = '''<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\r\n<html><head>\r\n<title>403 Forbidden</title>\r\n</head><body><h1>Access Refused</h1>\r\n<p>The requested URL was forbidden on this server.</p>\r\n</body></html>'''
                            erroMsg = constructMsg("403 Forbidden", errBd, get_content)
                            r.send(erroMsg)
                    else:
                        errBd = '''<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\r\n<html><head>\r\n<title>404 Not Found</title>\r\n</head><body><h1>Not Found</h1>\r\n<p>The requested URL was forbidden on this server.</p>\r\n</body></html>'''
                        erroMsg = constructMsg("404 Not Found", errBd, get_content)
                        r.send(erroMsg)

                    # r.close()

                    if r not in outputs:
                        outputs.append(r)
                else:
                    print('closing', addr)
                    if r in outputs:
                        outputs.remove(r)
                    inputs.remove(r)
                    r.close()


if __name__ == '__main__':
    port = int(sys.argv[1])
    # port = 8002
    main(port)
