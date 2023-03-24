import math
import random

#coding dictionary
#key is the character, value is the code
encoding_map = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'a': 10,
    'b': 11,
    'c': 12,
    'd': 13,
    'e': 14,
    'f': 15,
    'g': 16,
    'h': 17,
    'i': 18,
    'j': 19,
    'k': 20,
    'l': 21,
    'm': 22,
    'n': 23,
    'o': 24,
    'p': 25,
    'q': 26,
    'r': 27,
    's': 28,
    't': 29,
    'u': 30,
    'v': 31,
    'w': 32,
    'x': 33,
    'y': 34,
    'z': 35,
    ' ': 36,
}


#msg is a string
def preprocessing(msg):
    n = math.ceil(len(msg) / 5)
    list_of_msgs = []
    for i in range(n):
        if (i+1)*5 < len(msg):
            list_of_msgs.append(msg[i*5:(i+1)*5]) #this list now contains the 5 character strings
        else:
            s = msg[i*5:]
            s += ' ' * (5 - len(s)) #add spaces to the end of the string till it is 5 characters long
            list_of_msgs.append(s)
    return list_of_msgs
    
def encode(msg):
    list_of_msgs = preprocessing(msg)
    list_of_codes = [0] * len(list_of_msgs)
    for i in range(len(list_of_msgs)):
        for j in range(5):
            if list_of_msgs[i][j] in encoding_map:
                list_of_codes[i] += encoding_map[list_of_msgs[i][j]] * (37 ** (4-j))
            else:
                list_of_codes[i]+= 36 * (37 ** (4-j))
            
    return list_of_codes

def decode(list_of_codes):
    list_of_msgs = [0] * len(list_of_codes)
    for i in range(len(list_of_codes)):
        list_of_msgs[i] = ''
        for j in range(5):
            list_of_msgs[i] += list(encoding_map.keys())[list(encoding_map.values()).index((list_of_codes[i] // (37 ** (4-j))) % 37)]
    return list_of_msgs

def gcd(a, h):
    temp = 0
    while(1):
        temp = a % h
        if (temp == 0):
            return h
        a = h
        h = temp

    
def encrypt():
    q = 17
    p = 19
    n = q * p
    phi = (q-1) * (p-1)
    e = 2 #public key gcd(e, phie) = 1
    while (e < phi):
        # e must be co-prime to phi and
        # smaller than phi.
        if(gcd(e, phi) == 1):
            break
        else:
            e = e+1


def decrypt():
    pass

def main():
    
    msg = input("Enter the message: ")
    list_of_codes = encode(msg)
    print(list_of_codes)
    list_of_msgs = decode(list_of_codes)
    print(list_of_msgs)
    for i in range(len(list_of_msgs)):
        print(list_of_msgs[i], end = '')
    print()

main()