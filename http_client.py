import socket
import re
import sys
import io

err = {
    0: "Success.",
    1: "ERROR: Invalid input without 'http://'. ",
    2: "ERROR: Can't visit a 'https' page. ",
    3: "ERROR: Already 10 times of redirection. ",
    4: "ERROR: Response Code >= 400",
    5: "ERROR: Content-type is NOT 'text/html'. "
}


def checkStatCode(h, s, c):
    if "200 OK" in h:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=c)
        print(s)
        sys.exit(0)
    s_index = h.lower().find("HTTP/1.") + len("HTTP/1.")
    # print(h[s_index+3:s_index+6])
    if int(h[s_index + 3:s_index + 6]) >= 400:
        print(s)
        sys.exit(4)
    else:
        pass


def checkContentType(s):
    if s.find("text/html") == -1:
        sys.exit(5)
    else:
        pass


def findCharset(h):
    pattern = re.compile(b'charset=(.*)\r')
    if len(re.findall(pattern, h)) > 0:
        charset = re.findall(pattern, h)[0]
        return charset.decode()
    else:
        return 'utf-8'


def find_host(h):
    if "https" in h:
        sys.stderr.write("ERROR: Can't visit a 'https' page. \n")
        sys.exit(2)
    hostname = ''
    host_pattern_1 = re.compile(r'://(.*)/')
    host_pattern_2 = re.compile(r'://(.*):')
    host_pattern_3 = re.compile(r'://(.*)\r')
    host_pattern_4 = re.compile(r'://(.*)')
    if len(re.findall(host_pattern_1, h)) > 0:
        hostname = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', h)[0]
        if len(re.findall(host_pattern_4, h)) > 0:
            hostname = re.findall(host_pattern_4, hostname)[0]
    elif len(re.findall(host_pattern_2, h)) > 0:
        hostname = re.findall(host_pattern_2, h)[0]
    elif len(re.findall(host_pattern_3, h)) > 0:
        hostname = re.findall(host_pattern_3, h)[0]
    elif len(re.findall(host_pattern_4, h)) > 0:
        hostname = re.findall(host_pattern_4, h)[0]

    return hostname


def findLocation(s):
    new = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                     r'(?:%[0-9a-fA-F][0-9a-fA-F]))+', s)[0]
    sys.stderr.write("Redirected to:" + new + "\n")
    if "https" in new:
        sys.stderr.write("ERROR: Can't visit a 'https' page. \n")
        sys.exit(2)
    return new


def find_get_action(h):
    get_action = ''
    get_pattern_1 = re.compile(find_host(h) + '/(.*)')
    get_pattern_2 = re.compile(find_host(h) + '/(.*)\r')
    if len(re.findall(get_pattern_2, h)) > 0:
        get_action = re.findall(get_pattern_2, h)[0]
    elif len(re.findall(get_pattern_1, h)) > 0:
        get_action = re.findall(get_pattern_1, h)[0]
    return get_action


def port_num(h):
    port = 80
    pattern = re.compile(r'://(.*):')
    if len(re.findall(pattern, h)) > 0:
        port = int(re.findall(':(?:[\d])+', h)[0][1:])
    return port


def main(u):
    Get_action = find_get_action(u)
    Port_num = port_num(u)
    Host = find_host(u)
    count = 0
    while count < 10:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((Host, Port_num))
        s.send(('GET /' + Get_action + ' HTTP/1.0\r\nHost: ' + Host + '\r\n\r\n').encode())
        respond = []
        while True:
            d = s.recv(1024)
            if d:
                respond.append(d)
            else:
                break
        data = b''.join(respond)
        #if b'Content-Length:' in data:
        s.close()

        header, html = data.split(b'\r\n\r\n', 1)
        charset = findCharset(data)
        header_decode = header.decode(charset)
        html_decode = html.decode(charset)

        checkContentType(header_decode)
        checkStatCode(header_decode, html_decode,charset)
        # print(header_decode)
        move_per_301 = header_decode.find('301 Moved Permanently')
        move_per_302 = header_decode.find('302 Found')
        if move_per_301 == -1 & move_per_302 == -1:
            break
        redirect = findLocation(header_decode)
        Host = find_host(header_decode)
        Get_action = find_get_action(header_decode)
        Port_num = port_num(header_decode)
        count = count + 1
    if count == 10:
        sys.exit(3)


if __name__ == '__main__':

    #Url = input(":")
    Url = sys.argv[1]
    if "http://" not in Url:
        sys.exit(1)
    main(Url)
