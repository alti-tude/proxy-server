import threading
import socket
import blacklist as bl
import client_conn as cc

PORT = 20100

blacklist = bl.Blacklist()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('',PORT))
    s.listen(5)

    while True:
        conn, addr =  s.accept()
        t = threading.Thread(target=cc.handle_conn, args=(conn, addr, blacklist))
        t.start()

