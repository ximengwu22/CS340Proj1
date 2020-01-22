from socket import *
import sys
import re

stderr = {
    0: "Success.",
    1: "ERROR: Invalid input without 'http://'. ",
    2: "ERROR: Can't redirect to 'https'. ",
    3: "ERROR: Over 10 times of redirection. ",
    4: "ERROR: Response Code >= 400",
    5: "ERROR: Content-type is NOT 'text/html'. "
}

def checkStatCode(s):
    sindex = s.find("HTTP/1.") + len("HTTP/1.0 ") + 1
    if int(s[sindex:sindex+2]) >= 400:
        print(stderr[4])
        exit(4)
    elif "200 OK" in s:
        print(stderr[0])
        exit(0)
    else:
        pass


def checkContentType(s):
    if s.find("text/html") == -1:
        print(stderr[5])
        exit(5)
    else:
        pass

def findLocation(s):
    new = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                     r'(?:%[0-9a-fA-F][0-9a-fA-F]))+', s)[0]
    print("Redirected to:", new)
    if "https" in new:
        print(stderr[2])
        exit(2)
    return new

def getValidURL(s):
    return re.findall('https?://(?:[-\w.])+', s)[0]

def main(url, CN):
    serverPort = 80

    #Get valid URL: split serverName, cut 'http(s)://'
    serverName = getValidURL(url)

    # build connection
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    #clientSocket.listen(1)

    host = "Host: " + serverName + "\r\n\r\n"

    try:
        clientSocket.send("GET /icons/apache_pb2.gif HTTP/1.1\r\n".encode())
        clientSocket.send(host.encode())

    except error as e:
        print("ERROR: ",e)

    buffer = []
    buffer = ""
    while True:
        modifiedSentence = clientSocket.recv(1024)

        if modifiedSentence:
            print(modifiedSentence.decode())
            buffer += modifiedSentence.decode()
            #print("*",buffer)
        else:
            if "301 Moved" in buffer:
                dn = findLocation(buffer)
                clientSocket.close()
                main(dn,CN+1)
            checkContentType(buffer)
            break
    clientSocket.close()

if __name__ in '__main__':
    url = input('url:')
    if "http://" not in url:
        print(stderr[1])
        exit(1)
    main(url, 0)