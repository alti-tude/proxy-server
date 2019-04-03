import SimpleHTTPServer as sh
import SocketServer as ss
import os
import time
import sys
import threading
import logging

portRange = (10000, 10011)

class request_handler(sh.SimpleHTTPRequestHandler):
    def send_head(self):
        if self.command != "POST" and self.headers.get('If-Modified-Since', None):
            if "http" in self.path:
                filename = '/'.join(self.path.replace("://", "/").split('/')[2:])
            filename = filename.strip("/")
            
            if os.path.isfile(filename):
                a = time.gmtime(os.path.getmtime(filename))
                b = time.strptime(self.headers.get('If-Modified-Since', None), "%a, %d %b %Y %H:%M:%S %Z")
                print a, b
                if a < b:
                    self.send_response(304)
                    self.end_headers()
                    return None
        return SimpleHTTPServer.SimpleHTTPRequestHandler.send_head(self)

    def end_headers(self):
        self.send_header('Cache-control', 'must-revalidate')
        SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

    def do_POST(self):
        self.send_response(200)
        self.send_header('Cache-control', 'no-cache')
        SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

def run_server(port):
    print "starting server on port", port
    handler = sh.SimpleHTTPRequestHandler
    s = ss.ThreadingTCPServer(('', port), handler)
    s.allow_reuse_address = True
    s.serve_forever()

if __name__ == '__main__':
    t = ''
    for i in range(portRange[0], portRange[1]):
        t = threading.Thread(target=run_server, args=(i,))
        t.start()
    
    t.join()
