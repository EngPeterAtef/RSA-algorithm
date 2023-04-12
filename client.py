from main import *

PORT = 5050
ADDR = (SERVER, PORT)

_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message) #the length of the message in bytes
    send_length = str(msg_length).encode(FORMAT) #the length of the message in bytes encoded in bytes
    send_length += b' ' * (HEADER - len(send_length)) #padding the header with encoded spaces 
    _client.send(send_length) #send the header that contains the length of the message
    _client.send(message) #send the message



def handle_msg(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    # connected = True
    while True:
        msg = input("Enter your message (or type exit to end the connection): ").lower()
        if msg == "exit":
            send(DISCONNECT_MESSAGE)
            break
        list_of_ciphers = encryption(msg, (int(e), int(n)))
        str_number_of_ciphers_enc = str(encryption(str(len(list_of_ciphers)), (int(e), int(n))))
        print("str_number_of_ciphers_enc",str_number_of_ciphers_enc)
        send(str_number_of_ciphers_enc[1:len(str_number_of_ciphers_enc)-1])
        for i in range(len(list_of_ciphers)):
            send(str(list_of_ciphers[i]))
        print(_client.recv(2024).decode(FORMAT))
        print("typing....")
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
    conn.close()


print("[STARTING] client is starting...")
#create the keys
puplic_key , private_key = keyGeneration(512)
print("puplic_key",puplic_key)

_client.connect(ADDR)
#the keys of the server
e = _client.recv(2024).decode(FORMAT)
n = _client.recv(2024).decode(FORMAT)
print(f"e = {e} n = {n}")
print("patoraaa")
_client.send(str(puplic_key[0]).encode(FORMAT))
_client.send(str(puplic_key[1]).encode(FORMAT))


handle_msg(_client, ADDR)

