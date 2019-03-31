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

    connection_type = packetLines[0].split(' ')[0]
    return {"webserver": webserver, "port": port, "connection_type": connection_type}

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
    # s.sendall(data)
    print("---------------received client ----------------------")
    print(data.decode())
    print("-----------------------------------------------------")
    
    if header["connection_type"] == "CONNECT":
        d = 'HTTP/1.1 200 Connection established\r\n'
        conn.sendall(d.encode())
        try:
            conn.settimeout(4)
            data = conn.recv(1024)
        except Exception as e:
            print(e)
            conn.close()
            return
        print(data.decode())
        s.sendall(data)
        
    
    data = ""
    size = 0
    while True:
        chunk=""
        # recieve response from the external website
        try:
            s.settimeout(4)
            chunk = s.recv(256)
            s.settimeout(None)
        except Exception as e:
            print(e) 
            s.settimeout(None)
            break

        #send reponse back to the requesting client
        try:
            conn.settimeout(4)
            conn.send(chunk)
            conn.settimeout(None)
        except Exception as e:
            print(e) 
            conn.settimeout(None)
            break

        size += len(chunk.decode())
        data = data + chunk.decode()

        if len(chunk.decode()) == 0:
            break

    print("---------------received server ----------------------")
    print(data)
    print("size recvd ==== ", size)

    print("--------------------------------------------------")


    conn.close()

    print("connection closed to {0}".format(addr))