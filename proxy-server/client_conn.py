import socket
from node import Node



class Client(Node):
    def __init__(self, conn):
        Node.__init__(self,conn)

class Server(Node):
    def __init__(self):
        self.sock = socket.socket()
        super().__init__(self.sock)
        self.headers = {}
        self.request = ''
        self.response = ''


    def connect(self, request):
        self.headers = Node.parse_headers(self,request)
        ip = socket.gethostbyname(self.headers['webserver'])
        self.sock.connect((ip, self.headers['port']))
        
    def proc_request(self,request):
        self.request = request
        self.connect(request)
        
        ##check cache
        
        self.send_data(request)
        self.response = self.get_data()
    
    def get_response(self,request):
        self.proc_request(request)
        return self.response
        
        

# class handler():
#     def __init__(self, conn, addr):
#         self.client = conn
#         self.server = server_init(addr)        
#         self.timeout = 4

#     def server_init(self, addr):
#         data = 
#         header = parse_headers
#         self.server = socket.socket()
#         ip = socket.gethostbyname(header['webserver'])
#         self.server.connect((ip, header['port']))

#     def parse_headers(self, data):
#         print(data.decode())
#         packetLines = data.decode().split('\n')
        
#         webserver = ""
#         port = 80
#         for line in packetLines:
#             words = line.split(':')
#             if words[0] == 'Host':
#                 webserver = words[1].strip(' \r\n')
#                 if len(words)==3:
#                     port = int(words[2].strip(' \r\n'))
#         print(webserver, port)

#         connection_type = packetLines[0].split(' ')[0]
#         return {"webserver": webserver, "port": port, "connection_type": connection_type}

def handle_conn(conn, addr):
    '''
    handle connections to requesting clients
    forward to the actual external server
    send the response of the server back to the requesting client
    '''

    print("connected to {0}".format(addr))
    client = Client(conn)
    request = client.get_data()
    basic_auth = b'HTTP/1.1 401 not found\r\nContent-Length: 0\r\n\r\n'
    client.send_data(basic_auth)
    client.close()
    print(request)
    # server = Server()
    # response = server.get_response(request)
    # print(response)
    # client.send_data(response)
    # client.close()
    # server.close()
    # data = conn.recv(10000)
    
    # header = parse_headers(data)

    # #establish connection with the actual external website
    

    # print("---------------received client ----------------------")
    # print(data.decode())
    # print("-----------------------------------------------------")
    
    # if header["connection_type"] == "CONNECT":
    #     d = 'HTTP/1.1 200 Connection established\r\n'
    #     conn.sendall(d.encode())
    #     try:
    #         conn.settimeout(4)
    #         data = conn.recv(1024)
    #     except Exception as e:
    #         print(e)
    #         conn.close()
    #         return
    #     print(data.decode())
    #     s.sendall(data)
        
    
    # data = ""
    # size = 0
    # while True:
    #     chunk=""
    #     # recieve response from the external website
    #     try:
    #         s.settimeout(4)
    #         chunk = s.recv(256)
    #         s.settimeout(None)
    #     except Exception as e:
    #         print(e) 
    #         s.settimeout(None)
    #         break

    #     #send reponse back to the requesting client
    #     try:
    #         conn.settimeout(4)
    #         conn.send(chunk)
    #         conn.settimeout(None)
    #     except Exception as e:
    #         print(e) 
    #         conn.settimeout(None)
    #         break

    #     try:
    #         size += len(chunk.decode())
    #         data = data + chunk.decode()
    #     except:
    #         continue
    #     if len(chunk.decode()) == 0:
    #         break

    # print("---------------received server ----------------------")
    # print(data)
    # print("size recvd ==== ", size)
    # print("--------------------------------------------------")

    # conn.close()

    # print("connection closed to   {0}".format(addr))