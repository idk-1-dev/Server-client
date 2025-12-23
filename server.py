#all the information on this project is in the README file on my github page

import socket 
import threading
import time
import sys
import os

HEADER = 64
PORT = 5050
SERVER = '' #put local or private ip here MUST BE THE SAME IP ON BOTH FILES
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT = "!DISC"
DISCALL = "!DISCALL"

clients = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

def handle_client(conn,addr):
    print(f"\n✅[NEW CONNECTION] {addr} connected.")
    conn.send("What would you like to do (!DISC to quit) and (!DISCALL to end the server completely and remove clients), "
    "and another feature you can try, type 'enable ghost' and see what happens".encode(FORMAT))
    ghost_mode = False
    connected = True
    while connected:
        try:
            msg_len = conn.recv(HEADER).decode(FORMAT)
            if msg_len:
                msg_len = int(msg_len)
                msg = conn.recv(msg_len).decode(FORMAT)
                
                if msg == DISCONNECT:
                    connected = False
                    if ghost_mode:
                        print(f"\n❌[DISCONNECTED] [GHOST] has disconnected.")
                        break
                    print(f"\n❌[DISCONNECTED] {addr} has disconnected.")
                    sys.exit()
                    break
                if msg == DISCALL:
                    if ghost_mode:
                        print(f"\n[❌SERVER SHUTDOWN] by [GHOST]")
                        server.close()
                        os._exit(0)
                    print(f"\n[❌SERVER SHUTDOWN] by {addr}")
                    for c in clients:
                        try:
                            c.close()
                        except:
                            pass
                    server.close()
                    os._exit(0)
                if msg.lower() == "enable ghost":
                    ghost_mode = True   
                    conn.send("Ghost mode enabled".encode(FORMAT))
                    print(f"[GHOST] (???????) enabled ghost mode")
                    continue
                if ghost_mode:
                    print(f"\n[GHOST] {msg}")
                else:
                    print(f"\n[{addr[0]}:{addr[1]}] {msg}")
        except:
            pass
    conn.close()
def start():
    server.listen()
    time.sleep(1.5)
    print(f"✅[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client,args = (conn,addr))
        thread.start()
        print(f"✅[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ =='__main__':
    print("✅[STARTING] server is starting...")
    start()
