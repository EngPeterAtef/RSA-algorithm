import math
import random
import sys
# import time
import socket
# import threading
#constants
MAX_NUMBER_OF_DIGITS = len(str(sys.maxsize)) - 1 #=18
HEADER = 64 #size of the header in bytes that will contain the length of the message
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


#GLOBAL VARIABLES
#encoding dictionary
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

#FUNCTIONS
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

#list_of_msgs is a list of strings the output of the preprocessing function
def encode(list_of_msgs):
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
            #beutiful line of code
            list_of_msgs[i] += list(encoding_map.keys())[list(encoding_map.values()).index((list_of_codes[i] // (37 ** (4-j))) % 37)]
    return list_of_msgs


#function to check if a number is prime
def isPrime(n):
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False
        
    return True
    
#function to get a random prime number
def randPrime(seed,start,end):
    random.seed(seed) #to get different random numbers each time
    n = random.randint(start, end)
    while not isPrime(n):
        n = random.randint(start, end)
    return n

#msg_coded is the plaintext
def encrypt(msg_coded,e,n):
    msg_coded = int(msg_coded)
    c = modularExponent(msg_coded,e,n)
    return c

#this function get the gcd of 2 numbers and the coefficients of the linear combination
#where d = x*a + y*b
def ExtendedEuclidianAlgo(a, b):

	# base case
	if b == 0 :
		return a, 1, 0 # gcd(a,0) = a*1 + 0*0 = a
		
	d, x1, y1 = ExtendedEuclidianAlgo(b, a%b)
	
	x = y1
	y = x1 - (a//b) * y1
	
	return d, x, y
	
#this function solves the linear congruence equation ax = b (mod n)
def linearCongruence(A, B, N):
    A = A % N
    B = B % N
    #EXPLAINATION:
    #n/ ax - b
    #cn = ax -b
    #ax - kn = b => diofantine equation
    #condition for solution to exist: gcd(a,n) / b
    #d = gcd(A, N)
    #and d = u*A + v*N the gcd as linear combination of A and N where u and v are integers
    # let s = B/d
    # then x = s*u (mod N)
    # k = s*v (mod N)
    d, u, v = ExtendedEuclidianAlgo(A, N)
    
    # No solution exists if d does not divide b but in our case this will never happen
    # because b = 1 and d = gcd(e,phi(n)) = 1

    s = B // d
    x = (u * s) % N
    # k = (v * s) % N
    #make sure x is positive
    while (x < 0):
        x += N
    return x    
    
#this function generates the public and private keys
def keyGeneration():
    p = randPrime(0,10**(MAX_NUMBER_OF_DIGITS-1), 10**MAX_NUMBER_OF_DIGITS)
    q = randPrime(13,10**(MAX_NUMBER_OF_DIGITS-1), 10**MAX_NUMBER_OF_DIGITS)
    # p = 138014606015037877
    # q = 371821189834863247
    n = p * q
    phi = (q-1) * (p-1)
    e = 2 #public key gcd(e, phie) = 1
    while (e < phi):
        # e must be co-prime to phi and
        # smaller than phi.
        gcd = ExtendedEuclidianAlgo(e, phi)[0]
        if(gcd == 1):
            break
        else:
            e = e+1
    # Private key (d) using extended Euclid Algorithm
    d = linearCongruence(e, 1, phi)
    
    public_key = (e, n) #that will be sent to the sender for encryption
    private_key = (d, n) #will be used for decryption
    return public_key, private_key

#this function calculates a^e mod n        
def modularExponent(a, e, n):
    e = bin(e)[2:]#because the first two characters are 0b
    e = e[::-1]#reverse the string
    x = 1#the result
    for i in range(len(e)):
        if e[i] == '1':
            x = x * a % n
        a = a * a % n
    return x

#msg_cipher is the ciphertext
def decrypt(msg_cipher, d, n):
    msg_cipher = int(msg_cipher)
    m = modularExponent(msg_cipher, d, n)
    return m

def encryption(msg,public_key):
    list_of_blocks = preprocessing(msg)
    # print("list_of_blocks",list_of_blocks)
    list_of_codes = encode(list_of_blocks)
    # print("list_of_codes",list_of_codes)
    list_of_ciphers = [0] * len(list_of_codes)
    for i in range(len(list_of_codes)):
        list_of_ciphers[i] = encrypt(list_of_codes[i], public_key[0], public_key[1])
    # print("list_of_ciphers",list_of_ciphers)
    return list_of_ciphers

def decryption(private_key,list_of_ciphers):
    list_of_decoded = [0] * len(list_of_ciphers)
    for i in range(len(list_of_ciphers)):
        list_of_decoded[i] = decrypt(list_of_ciphers[i], private_key[0], private_key[1])
    # print("list_of_decoded",list_of_decoded)
    list_of_msgs = decode(list_of_decoded)
    print(list_of_msgs)
    for i in range(len(list_of_msgs)):
        print(list_of_msgs[i], end = '')
    print()
    return list_of_msgs



