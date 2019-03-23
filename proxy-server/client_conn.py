import socket

def parse_headers(data):
    print(data.decode())
    packetLines = data.decode().split('\n')
    # locationOnSever = packetLines[0].split(' ')[1]
    
    webserver = ""
    port = 80
    for line in packetLines:
        words = line.split(':')
        if words[0] == 'Host':
            webserver = words[1].strip(' \r\n')
            if len(words)==3:
                port = int(words[2].strip(' \r\n'))
    print(webserver, port)#, locationOnSever)

    return {"webserver": webserver, "port": port}#, "location_on_server":locationOnSever}

def handle_conn(conn, addr):
    print("connected to {0}".format(addr))
    while True:
        data = conn.recv(10000)
        
        header = parse_headers(data)

        s = socket.socket()
        ip = socket.gethostbyname(header['webserver'])
        s.connect((ip, header['port']))
        s.sendall(data)
        print(data.decode())
        data = ""
        while True:
            print(ip)
            chunk = s.recv(1024)
            if len(chunk) == 0:
                break
            data = data+chunk.decode()
            print(data)
        conn.sendall(data.encode())
    conn.close()
    print("connection closed to {0}".format(addr))