from main import *
#constants
PORT = 5050
ADDR = (SERVER, PORT)

_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_server.bind(ADDR)

#received data
list_of_ciphers = []


def send(conn,msg):
    message = msg.encode(FORMAT)
    msg_length = len(message) #the length of the message in bytes
    send_length = str(msg_length).encode(FORMAT) #the length of the message in bytes encoded in bytes
    send_length += b' ' * (HEADER - len(send_length)) #padding the header with encoded spaces 
    conn.send(send_length) #send the header that contains the length of the message
    conn.send(message) #send the message

    #this function is called when a client connects to the server
#it handles the client
#this function runs for each client in separate threads
def handle_msg(conn, addr,e,n):
    print(f"[NEW CONNECTION] {addr} connected.")
    # connected = True
    while True:
        #receive the header that contains the length of the message
        msg_length = conn.recv(HEADER).decode(FORMAT)
        list_of_ciphers = []
        #if the header is empty, the client has disconnected
        if msg_length:
            msg_length = int(msg_length)
            #receive the actual message
            msg = conn.recv(msg_length).decode(FORMAT)
            #to handle disconnection
            if msg == DISCONNECT_MESSAGE:
                break
            length_ciphers = decryption(private_key,[int(msg)])
            print("length_ciphers",length_ciphers)
            list_of_ciphers = []
            for i in range(int(length_ciphers)):
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    #receive the actual message
                    msg = conn.recv(msg_length).decode(FORMAT)
                    #to handle disconnection
                    if msg == DISCONNECT_MESSAGE:
                        break
                    list_of_ciphers.append(int(msg))
            res = decryption(private_key,list_of_ciphers)
            print(res)
            print("-----------------------------------------")
            conn.send("MSG RECEIVED".encode(FORMAT))
        msg = input("Enter your message (or type exit to end the connection): ").lower()
        if msg == "exit":
            send(conn,DISCONNECT_MESSAGE)
            break
        list_of_ciphers = encryption(msg, (int(e), int(n)))
        # send(conn,str(len(list_of_ciphers)))
        str_number_of_ciphers_enc = str(encryption(str(len(list_of_ciphers)), (int(e), int(n))))
        print("str_number_of_ciphers_enc",str_number_of_ciphers_enc)
        send(conn,str_number_of_ciphers_enc[1:len(str_number_of_ciphers_enc)-1])
        for i in range(len(list_of_ciphers)):
            send(conn,str(list_of_ciphers[i]))
        print(conn.recv(2024).decode(FORMAT))
        print("typing....")
    conn.close()

def start_listening():
    _server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = _server.accept() #blocking line so we will wait till a client connects
        conn.send(str(puplic_key[0]).encode(FORMAT))
        conn.send(str(puplic_key[1]).encode(FORMAT))
        e = conn.recv(2024).decode(FORMAT)
        n = conn.recv(2024).decode(FORMAT)
        # thread = threading.Thread(target=handle_msg, args=(conn, addr,e,n))
        # thread.start()
        #the number of active connections is the number of threads
        # print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}") # -1 because of the main thread
        print(f"e = {e} n = {n}")
        handle_msg(conn, addr,e,n)
        


puplic_key , private_key = keyGeneration(512)
print("puplic_key",puplic_key)
print("[STARTING] server is starting...")
start_listening()