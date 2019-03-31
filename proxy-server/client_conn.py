import socket

def parse_headers(data):
    print(data.decode())
    packetLines = data.decode().split('\n')
    
    webserver = ""
    port = 80
    for line in packetLines:
        words = line.split(':')
        if words[0] == 'Host':
            webserver = words[1].strip(' \r\n')
            if len(words)==3:
                port = int(words[2].strip(' \r\n'))
    print(webserver, port)

    return {"webserver": webserver, "port": port}

def handle_conn(conn, addr):
    '''
    handle connections to requesting clients
    forward to the actual external server
    send the response of the server back to the requesting client
    '''

    print("connected to {0}".format(addr))
    data = conn.recv(10000)
    
    header = parse_headers(data)

    #establish connection with the actual external website
    s = socket.socket()
    ip = socket.gethostbyname(header['webserver'])
    s.connect((ip, header['port']))
    s.sendall(data)
    print("---------------received client ----------------------")
    print(data.decode())
    
    # recieve response from the external website
    data = ""
    while True:
        chunk = s.recv(1024)
        conn.send(chunk)
        # print(data)
        if len(chunk) < 1024:
            break

    print("---------------received server ----------------------")
    print(data)
    #send reponse back to the requesting client
    # conn.sendall(data.encode())

    conn.close()

    print("connection closed to {0}".format(addr))