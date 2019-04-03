import threading
import socket
import base64
import blacklist as bl
import client_conn as cc
from cache import Cache

PORT = 20100

blacklist = bl.Blacklist()

auth_users = [b"trial:trial", b"something:something"]
auth_users = [base64.b64encode(x) for x in auth_users]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('',PORT))
    s.listen(5)

    cache = Cache()
    while True:
        conn, addr =  s.accept()
        t = threading.Thread(target=cc.handle_conn, args=(conn, addr, blacklist, auth_users, cache))
        t.start()

