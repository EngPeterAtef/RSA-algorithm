from main import *

PORT = 5050
ADDR = (SERVER, PORT)

_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message) #the length of the message in bytes
    send_length = str(msg_length).encode(FORMAT) #the length of the message in bytes encoded in bytes
    send_length += b' ' * (HEADER - len(send_length)) #padding the header with encoded spaces 
    _client.send(send_length) #send the header that contains the length of the message
    _client.send(message) #send the message
    print(_client.recv(2024).decode(FORMAT))



#this function is called when a client connects to the server
#it handles the client
#this function runs for each client in separate threads
# def handle_server(conn, addr):
#     print(f"[NEW CONNECTION] {addr} connected.")
#     connected = True
#     while connected:
#         #receive the header that contains the length of the message
#         msg_length = conn.recv(HEADER).decode(FORMAT)
#         #if the header is empty, the client has disconnected
#         if msg_length:
#             msg_length = int(msg_length)
#             #receive the actual message
#             msg = conn.recv(msg_length).decode(FORMAT)
#             print(f"[{addr}] {msg}")
#             print("-----------------------------------------")
            
#             #to handle disconnection
#             if msg == DISCONNECT_MESSAGE:
#                 connected = False
#     conn.close()

# def start_listening():
#     _client.listen()
#     print(f"[LISTENING] Client is listening on {SERVER}")
#     while True:
#         conn, addr = _client.accept()
#         thread = threading.Thread(target=handle_server, args=(conn, addr))
#         thread.start()
#         #the number of active connections is the number of threads
#         print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}") # -1 because of the main thread

e = _client.recv(2024).decode(FORMAT)
n = _client.recv(2024).decode(FORMAT)

while True:
    msg = input("Enter your message (or type exit to end the connection): ")
    if msg == "exit":
        send(DISCONNECT_MESSAGE)
        break
    list_of_ciphers = encryption(msg, (int(e), int(n)))
    send(str(list_of_ciphers))
