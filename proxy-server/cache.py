import time
import urllib.request
import client_conn as cc
import blacklist as bl
import base64
import socket
from copy import deepcopy

portRange = (10000, 10011)

class Cache:
    """ LRU cache """

    def __init__(self, max_size=3):
        self.cache = {}
        print("cache innit")
        self.request_count = {}
        self.MAX_SIZE = max_size
    

    def get_cache(self, server, request):
        """
        Get cached request
        """
        if request in self.cache:
            timestamp = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(self.cache[request]['access_time']))
            check_request = request.decode().replace('\r\n', '\n').split('\n')
            check_request.insert(-2, 'If-Modified-Since: %s' % timestamp)
            check_request = '\r\n'.join(check_request).encode()
            resp = server.get_response(check_request).decode().split('\r\n')[0]
            print(check_request)
            if '304' in resp:
                self.cache[request]['access_time'] = time.time()
                return self.cache[request]['content']
            elif '200' in resp:
                del self.cache[request]
            else:
                print("ERROR: Could not retrieve URL")

        return None
    
    def get_access_time(self,request):
        if request in self.cache:
            return self.cache[request]['access_time']
        return None

    def set_cache(self, request, content):
        """
        Add / Update value to cache
        """
        if request not in self.cache and len(self.cache) >= self.MAX_SIZE:
            self.remove_lru()
        self.cache[request] = {'access_time':time.time(), 'content':content}


    def update(self, request, content):
        """
        Cache all requests made thrice in last 5 minutes, else remove
        """
        self.clear_request_count()
        
        if request not in self.request_count:
            self.request_count[request] = {'request_time':time.time(), 'count':1}
        else:
            if self.request_count[request]['count'] < 2:
                self.request_count[request]['count'] += 1
            else:
                self.set_cache(request, content)
                del self.request_count[request]
        print(self.request_count)
        return


    def clear_request_count(self):
        """
        Remove all requests not made thrice in last 5 minutes
        """
        d = {}
        for request in list(self.request_count):
            if not (
                    time.time() - self.request_count[request]['request_time'] >= 5*60 and
                    self.request_count[request]['count'] < 3
                ):
                d[request] = self.request_count[request]
        self.request_count = d
        return


    def remove_lru(self):
        """
        Remove least recently used cache
        """
        oldest_request = None
        for request in self.cache:
            if (
                    oldest_request is None or
                    self.cache[request]['access_time'] < self.cache[oldest_request]['access_time']
                ):
                oldest_request = request
        del self.cache[oldest_request]

if __name__ == "__main__":
    blacklist = bl.Blacklist()

    auth_users = [b"trial:trial", b"something:something"]
    auth_users = [base64.b64encode(x) for x in auth_users]
    cache = Cache()
    server = cc.Server(blacklist, auth_users)
    while True:
        msg = [
            'GET /server.py HTTP/1.1\r\n',
            'Host: localhost:10010\r\n',
            'User-Agent: curl/7.58.0\r\n',
            'Accept: */*\r\n\r\n',
        ]

        msg = ''.join(msg).encode()

        resp = cache.get_cache(server,msg)
        if resp == None:
            cache.update(msg, server.get_response(msg)) 

        print(resp)
        # print(cache.cache)
        # print(cache.request_count)
        time.sleep(2)
