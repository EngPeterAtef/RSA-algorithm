from main import *
#constants
PORT = 5050
ADDR = (SERVER, PORT)

_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_server.bind(ADDR)

#received data
list_of_ciphers = []


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message) #the length of the message in bytes
    send_length = str(msg_length).encode(FORMAT) #the length of the message in bytes encoded in bytes
    send_length += b' ' * (HEADER - len(send_length)) #padding the header with encoded spaces 
    _server.send(send_length) #send the header that contains the length of the message
    _server.send(message) #send the message

    #this function is called when a client connects to the server
#it handles the client
#this function runs for each client in separate threads
def handle_msg(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    # connected = True
    while True:
        #receive the header that contains the length of the message
        msg_length = conn.recv(HEADER).decode(FORMAT)
        list_of_ciphers.clear()
        #if the header is empty, the client has disconnected
        if msg_length:
            msg_length = int(msg_length)
            #receive the actual message
            msg = conn.recv(msg_length).decode(FORMAT)
            #to handle disconnection
            if msg == DISCONNECT_MESSAGE:
                break
            tempList = msg.split(",")
            print("tempList",tempList)
            if len(tempList) == 1:
                if tempList[0] != '[]': #to handle the case of empty string sent by the client
                    list_of_ciphers.append(int(tempList[0][1:len(tempList[0])-1]))
                
            else:
                for i in range(len(tempList)):
                    if i==0:
                        list_of_ciphers.append(int(tempList[i][1:]))
                    elif i==len(tempList)-1:
                        list_of_ciphers.append(int(tempList[i][:len(tempList[i])-1]))
                    else:
                        list_of_ciphers.append(int(tempList[i]))
            decryption(private_key,list_of_ciphers)
            # print(f"[{addr}] {msg}")
            print("-----------------------------------------")
            conn.send("MSG RECEIVED".encode(FORMAT))
    conn.close()

def start_listening():
    _server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = _server.accept() #blocking line so we will wait till a client connects
        # thread = threading.Thread(target=handle_msg, args=(conn, addr))
        # thread.start()
        #the number of active connections is the number of threads
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}") # -1 because of the main thread
        conn.send(str(puplic_key[0]).encode(FORMAT))
        conn.send(str(puplic_key[1]).encode(FORMAT))
        e = conn.recv(2024).decode(FORMAT)
        n = conn.recv(2024).decode(FORMAT)
        print(f"e = {e} n = {n}")
        handle_msg(conn, addr)



puplic_key , private_key = keyGeneration()
print("[STARTING] server is starting...")
start_listening()