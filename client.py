import socket 
import threading
import os

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT = "!DISC"
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
DISCALL = "!DISCALL"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
msg_server=client.recv(2048).decode(FORMAT)
print(msg_server)
def listen_server():
    try:
        while True:
            data = client.recv(2048)
            if not data:
                raise ConnectionError
    except ConnectionError:
        print("\n[❌CONNECTION ERORR] server closed the connection.")
        os._exit(0)
    except:
        print("\n[❌SERVER CLOSED] connection lost.")
        os._exit(0)
threading.Thread(target=listen_server, daemon=True).start()

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    try:
        client.send(send_len)
        client.send(message)
    except BrokenPipeError:
        print("[❌SERVER CLOSED] the server has shut down")
        exit()

if __name__ == '__main__':
    while True:
        msg = str(input("\nEnter message: "))
        send(msg)
        if msg == "enable ghost":
            print("Ghost enabled.")

        if msg not in ["enable ghost",DISCONNECT,DISCALL]:
            print("Message sent.")

        if msg == DISCONNECT:
            print("[❌DISCONNECTED] from the server.")
            break

        if msg == DISCALL:
            print("[❌SERVER SHUTDOWN] initiated.")
            break
