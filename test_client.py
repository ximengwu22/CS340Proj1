# !/usr/bin/env python

from socket import *

if "__main__" == __name__:
    serverName = 'localhost' #https://tools.ietf.org/html/rfc2616
    sock = socket(AF_INET, SOCK_STREAM);
    sock.connect((serverName, 8001))
    sock.send("rfc2616.xt".encode())

    szBuf = sock.recv(1024)

    print("-Start Receiving-")
    print(szBuf.decode())

    sock.close()
    print("-End of connect-")
