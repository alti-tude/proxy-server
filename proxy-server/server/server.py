import SocketServer as ss
import time
import threading
import logging
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import os
import sys

class S(BaseHTTPRequestHandler):
    def _set_headers(self, resp):
        self.send_response(resp)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        filename = ""
        if "http" in self.path:
            filename = '/'.join(self.path.replace("://", "/").split('/')[2:])
        filename = filename.strip("/")
        self.log_message(filename)
        if self.headers.get('If-Modified-Since', None):

            if os.path.isfile(filename):
                a = time.gmtime(os.path.getmtime(filename))
                b = time.strptime(self.headers.get('If-Modified-Since', None), "%a, %d %b %Y %H:%M:%S %Z")
                print a, b
                if a < b:
                    self.send_response(304)
                    self.end_headers()
                    return None
                else:
                    self.send_response(200)
                    self.end_headers()
                    return None

        self._set_headers(200)
        if os.path.isfile(filename):
            fil = open(filename, "rb")
            data = b''
            while True:
                chunk = fil.read()
                if not chunk:
                    break
                self.wfile.write(chunk)
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers(200)
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, S)
    print 'Starting httpd...', port
    httpd.serve_forever()

if __name__ == "__main__":
    run(int(sys.argv[1]))
    
