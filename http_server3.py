from socket import *
import json
import sys
import re

def checkParamInt(s):
    a = s[s.find("a=") + 2:s.find("&b")]
    b = s[s.find("b=")+2:s.find("&an")]
    if s[len(s) - 1] == '/':
        c = s[s.find("er=") + 3:len(s) - 2]
    else:
        c = s[s.find("er=") + 3:]
    return is_number(a) and is_number(b) and is_number(c)


def is_number(x):
    try:
        float(x)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(x)
        return True
    except (TypeError, ValueError):
        pass
    return False

def checkURL(s):
    return "/product" in s

def getProduct(s):
    a = float(s[s.find("a=")+2:s.find("&b")])
    b = float(s[s.find("b=")+2:s.find("&an")])
    if s[len(s)-1] == '/':
        c = float(s[s.find("er=")+3:len(s)-2])
    else:
        c = float(s[s.find("er=")+3:])
    prod = a * b * c
    return a,b,c,prod

def parse2Json(a,b,c,prod):
    stc = {
        "operation": "product",
        "operands": [a, b, c],
        "result": prod
    }
    rs = json.dumps(stc,indent=4)
    return rs

def constructMsg(s,body):
    header = '''HTTP/1.1 %s\r\nContent-Type: application/json\r\n\r\n'''% s
    header += body
    return header.encode()

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

        print("-response::", respBuf)


        if checkURL(respBuf):
            if checkParamInt(respBuf):
                [a, b, ano, prod] = getProduct(respBuf)
                res = parse2Json(a, b, ano, prod)
                rs = constructMsg("200 OK", res)
                connSocket.send(rs)
            else:
                erroMsg = '''<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\r\n<html><head>\r\n<title>400 Bad Request</title>\r\n</head><body><h1>Illegal Parameters</h1>\r\n<p>Oops...</p>\r\n</body></html>'''
                msg = constructMsg("400 Bad Request", erroMsg)
                connSocket.send(msg)

        else:
            erroMsg = '''<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\r\n<html><head>\r\n<title>404 Not Found</title>\r\n</head><body><h1>Not Found</h1>\r\n<p>Oops...</p>\r\n</body></html>'''
            msg = constructMsg("404 Not Found", erroMsg)
            connSocket.send(msg)

        connSocket.close()

if __name__ in '__main__':
    inp = int(sys.argv[1])
    # port = re.findall(':(?:[\d])+', inp)
    main(inp)