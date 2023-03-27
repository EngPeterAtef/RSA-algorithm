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
        send(str(list_of_ciphers))
        print(_client.recv(2024).decode(FORMAT))
        print("typing....")
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
            res = decryption(private_key,list_of_ciphers)
            print(res)
            # print(f"[{addr}] {msg}")
            print("-----------------------------------------")
            conn.send("MSG RECEIVED".encode(FORMAT))
    conn.close()


print("[STARTING] client is starting...")
#create the keys
puplic_key , private_key = keyGeneration(1024)
_client.connect(ADDR)
#the keys of the server
e = _client.recv(2024).decode(FORMAT)
n = _client.recv(2024).decode(FORMAT)
print(f"e = {e} n = {n}")

_client.send(str(puplic_key[0]).encode(FORMAT))
_client.send(str(puplic_key[1]).encode(FORMAT))


handle_msg(_client, ADDR)

