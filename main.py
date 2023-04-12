#Imports
import math
# import random
from Crypto.Util import number
import os
import socket

#constants
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
# def isPrime(n):
#     for i in range(2,int(n**0.5)+1):
#         if n%i==0:
#             return False
        
#     return True
#function to get a random prime number
# def randPrime(seed,n):
#     random.seed(seed) #to get different random numbers each time
#     num = random.randint(2**(n-1)+1, 2**n-1)
#     while not isPrime(num):
#         # n = random.randint(start, end)
#         num = random.randint(2**(n-1)+1, 2**n-1)
#     return num

#msg_coded is the plaintext
def encrypt(msg_coded,e,n):
    msg_coded = int(msg_coded)
    c = modularExponent(msg_coded,e,n)
    return c

#msg_cipher is the ciphertext
def decrypt(msg_cipher, d, n):
    msg_cipher = int(msg_cipher)
    m = modularExponent(msg_cipher, d, n)
    return m

#this function get the gcd of 2 numbers and the coefficients of the linear combination(x,y)
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
def keyGeneration(n_bits):
    #number.getPrime(number of bits, random function)
    #for n bits it will generate prime with 2^n <= p < 2^(n+1)
    q = number.getPrime(n_bits, os.urandom)
    p = number.getPrime(n_bits, os.urandom)
    while p == q: 
        p = number.getPrime(n_bits, os.urandom)
    # print(f"p = {p} and q = {q}")
    n = p * q
    phi = (q-1) * (p-1)
    print(f"phi = {phi}")
    l = len(bin(phi)[2:])#this is the number of bits in phi
    # print(f"l = {l}")
    # we will initialize e to a random prime whose length is half of the length of phi
    # the initial value will not always be co-prime to phi
    # so we will increment it till we find a co-prime
    e = number.getPrime(l//2, os.urandom)
    while (e < phi):
        # e must be co-prime to phi and
        # smaller than phi.
        print(f"e = {e}")
        gcd = ExtendedEuclidianAlgo(e, phi)[0]
        if(gcd == 1):
            break
        else:
            e = e+1
            if e==phi:
                e = 2
    # Private key (d) using extended Euclid Algorithm
    d = linearCongruence(e, 1, phi)
    
    public_key = (e, n) #that will be sent to the sender for encryption
    private_key = (d, n) #will be used for decryption
    return public_key, private_key

#this function calculates a^e mod n        
def modularExponent(a, e, n):
    e = bin(e)[2:]#because the first two characters are 0b
    # print("e",e)
    # print("e[0]",e[0])
    e = e[::-1]#reverse the string
    # print("e",e)
    # print("e[0]",e[0])
    x = 1#the result
    a = a % n
    for i in range(len(e)):
        # print(f"x = {x} and a = {a} , e[i] = {e[i]}")
        if e[i] == '1':
            x = x * a % n
        a = a * a % n

    return x


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
    # print(list_of_msgs)
    res = ""
    for i in range(len(list_of_msgs)):
        res += list_of_msgs[i]
        # print(list_of_msgs[i], end = '')
    # print()
    return res

# this function performs the fermat factoring algorithm to find the factors of n
def fermatFactoringAlgo(n: int):
    # find the square root of n
    k = math.ceil(math.sqrt(n))
    # find the square of k
    h_square = k * k - n
    # find the square root of h_square
    h = int(math.sqrt(h_square))
    # while the square of h is not equal to h_square
    while h * h != h_square:
        # increase a by 1
        k = k + 1
        # find the square of k
        h_square = k * k - n
        # find the square root of h_square
        h = int(math.sqrt(h_square))
    # return the factors
    return k - h, k + h
