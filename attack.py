from main import *

# c is the ciphertext
# p is the plaintext
# e and n are the public key
# this function performs the brute-force attack using the public key
def attack(c: list[int], p: str, n: int,s:int,e:int):
    global results
    # the range of the key is from 1 to n
    for d in range(s, e):
        # print(f"trying d = {d}")
        # if the plaintext is equal to the ciphertext

        x = decryption((d, n), c)
        if x.__contains__(p):
            # return the private key
            results.append(d)
    #         return d
    # # if the private key is not found
    # return -1


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

if __name__ == "__main__":
    # the plaintext
    msg = "hello worldz"
    # the public key and the private key
    public_key, private_key = keyGeneration(14) #min number of bits is 14 34an al encryption wel decryption y4t8lo
    print(f"public_key = {public_key} and private_key = {private_key}")
    # the ciphertext
    c = encryption(msg, public_key)
    # the private key
    threads = [None] * 10
    results = []
    for i in range(len(threads)):
        threads[i] = threading.Thread(target=attack, args=(c, msg,public_key[1],1+i*public_key[1]//10, (i+1)*public_key[1]//10 +1))
        threads[i].start()
    # d = attack(c, msg, public_key[1])
    # print the private key
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}") # -1 because of the main thread
    res = 0
    for i in range(len(threads)):
        print(f"thread {i} is alive")
        threads[i].join()
        # if results[i] > res:
        #     res = results[i]
            # break
    print(f"private_key = {results}")