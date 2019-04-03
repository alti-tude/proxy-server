import socket
from node import Node



class Client(Node):
    def __init__(self, conn):
        Node.__init__(self,conn)


class Server(Node):
    def __init__(self, blacklist, auth_users, cache):
        self.sock = socket.socket()
        super().__init__(self.sock)
        self.headers = {}
        self.request = ''
        self.response = ''
        self.blacklist = blacklist
        self.auth_users = auth_users
        self.cache = cache

    def connect(self, ip):
        self.sock.close()
        self.sock = socket.socket()
        self.sock.connect((ip, self.headers['port']))
        
    def proc_request(self,request):
        self.request = request
        self.headers = Node.parse_headers(self, request)

        #check blacklist
        ip = socket.gethostbyname(self.headers['webserver'])
        if self.blacklist.blacklisted(ip) and self.headers['auth'] not in self.auth_users:
            return None
        
        #check cache
        if self.headers['conn_type'] == 'GET':
            print(self.cache.request_count)
            self.response = self.cache.get_cache(Server(self.blacklist, self.auth_users, self.cache),self.request)
            if self.response:
                self.cache.update(self.request, self.response)
                print("from cache-------", self.response[0:10])
                return self.response
        
        self.connect(ip)
        self.send_data(request)
        self.response = self.get_data()
        self.cache.update(self.request, self.response)

        return self.response

    def get_response_full(self,request):
        return self.proc_request(request)
    
    def get_response(self, request):
        self.request = request
        self.headers = Node.parse_headers(self, request)

        ip = socket.gethostbyname(self.headers['webserver'])
        self.connect(ip)        
        self.send_data(request)
        self.response = self.get_data()
        return self.response

    def close(self):
        self.sock.close()
        self.sock = socket.socket()

        
        

def handle_conn(conn, addr, blacklist, auth_users, cache):
    '''
    handle connections to requesting clients
    forward to the actual external server
    send the response of the server back to the requesting client
    '''

    print("connected to {0}".format(addr))
    client = Client(conn)

    # if addr[1] < 20000 or addr[1] > 20099:
    #     print("[*] Restricted address ", addr[1])
    #     client.send_data(b'Restricted access\n')
    #     client.close()
    #     return

    server = Server(blacklist, auth_users, cache)
    # while True:
    request = client.get_data()
    if len(request.decode()) == 0:
        return
    
    print("request from client----------")
    print(request)

    response = server.get_response_full(request)
    if not response:
        print("ACCESS TO WEBSITE BLOCKED")
        client.send_data(b'HTTP/1.1 401 ACCESS BLOCKED\r\n\r\n<body>ACCESS DENIED</body>')
    else:  
        client.send_data(response)
    
    client.close()
   