from socket import *

from pip._vendor.distlib.compat import raw_input

if "__main__" == __name__:
    serverName = 'localhost' #https://tools.ietf.org/html/rfc2616
    sock = socket(AF_INET, SOCK_STREAM);
    sock.connect((serverName, 8880))

    while True:
        inp = raw_input("please input:").encode()
        sock.sendall(inp)
        szBuf = sock.recv(1024)

        print("-Start Receiving-")
        print(szBuf.decode())

        sock.close()
        print("-End of connect-")