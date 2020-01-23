from socket import *
from os import path
import re
import sys


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
    try:
        serverSocket.bind(("", serverPort))
        serverSocket.listen(1)
    except error:
        print(error)

    while True:
        connSocket, addr = serverSocket.accept()  # connSocket: NEW CONNECTION SOCKET
        # connSocket.settimeout(10)

        respBuf = connSocket.recv(1024).decode()

        # print(respBuf)
        get_content = getAction(respBuf)

        if checkFileExist(get_content):
            if checkEndWith(get_content):
                corrMsg = constructMsg("200 OK", '', get_content)
                connSocket.send(corrMsg)
            else:
                errBd = '''<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\r\n<html><head>\r\n<title>403 Forbidden</title>\r\n</head><body><h1>Access Refused</h1>\r\n<p>The requested URL was forbidden on this server.</p>\r\n</body></html>'''
                erroMsg = constructMsg("403 Forbidden", errBd, respBuf)
                connSocket.send(erroMsg)
        else:
            errBd = '''<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\r\n<html><head>\r\n<title>404 Not Found</title>\r\n</head><body><h1>Not Found</h1>\r\n<p>The requested URL was forbidden on this server.</p>\r\n</body></html>'''
            erroMsg = constructMsg("404 Not Found", errBd, respBuf)
            connSocket.send(erroMsg)

        connSocket.close()


if __name__ == '__main__':
    #port = int(sys.argv[1])
    main(8000)
