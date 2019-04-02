import socket

class Node():
    def __init__(self, conn):
        self.sock = conn
        self.chunkSize = 1024
        self.timeout = 2
        
    def get_data(self):
        data = b''
        while True:
            try:
                self.sock.settimeout(2)
                chunk = self.sock.recv(self.chunkSize)
                self.sock.settimeout(None)
            except Exception as e:
                print(e)
                self.sock.settimeout(None)
                break

            data = data+chunk
        
        return data
    
    def send_data(self, data):
        try:
            self.sock.sendall(data)
        except Exception as e:
            print(e)
            return False
        return True

    def close(self):
        self.sock.close()
    
    def parse_headers(self, data):
        packetLines = data.decode().split('\n')

        webserver = ""
        port = 80
        headers = {}
        for line in packetLines:
            words = line.split(':')
            if len(words)==0:
                break

            if words[0] == 'Host':
                webserver = words[1].strip(' \r\n')
                if len(words)==3:
                    port = int(words[2].strip(' \r\n'))
            elif len(words) == 2:
                headers[words[0]] = words[1]

        print(webserver, port)
        headers['first_line'] = packetLines[0]
        headers['webserver'] = webserver
        headers['port'] = port

        return headers