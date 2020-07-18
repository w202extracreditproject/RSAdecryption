#Extra Credit Project 
#
#Tool to decrypt an encrypted message and 
#find the value of the encrypted message
#Allows RSA to be cracked through encryption key pairs

#python library that generates pseudo-random numbers to generate key pairs
import random

#Euclid's algorithm will be used later to ensure that e and phi(n) are comprime
#and to generate private keys
def gcd(i, j):
    while j != 0:
        i, j = j, i % j
    return i

#Using multiplicative inverse to find Euclid's extened algorithm 
def extended_euclid(e, phi):
    a = 0
    b = 0
    c = 1
    d = 1
    temp_phi = phi
    
    #loop that iterates when e is greater than 0
    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = c- temp1 * b
        y = a - temp1 * d
        
        c = b
        b = x
        a = d
        d = y
    
    if temp_phi == 1:
        return a + phi

#Checks if the numbers inputed are prime
def prime_check(num):

    #checks for the smallest prime number
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in xrange(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

#Generates a keypair through a psuedo-random number generator
def generate_keypair(p, q):
    if not (prime_check(p) and prime_check(q)):
        #raises an error if p or q is not prime
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        #p and q need to be two distinct prime values
        raise ValueError('p and q cannot be equal')
    #n = pq
    n = p * q

    #phi is totient of n
    phi = (p-1) * (q-1)

    #Psuedo random number chosen so e and phi(n) are coprime 
    e = random.randrange(1, phi)

    #Euclid's Algorithm used to check e and phi(n) are coprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    #Extended Euclid's Algorithm used to generate a private key
    a = extended_euclid(e, phi)
    
    #Returns a  public and private keypairs 
    #Public key is (e, n)
    #Private key is (a, n)
    return ((e, n), (a, n))

def encrypt(pk, plaintext):
    #Encrypts the plaintext
    key, n = pk
    #Convert each letter in the plaintext using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    #Returns an array of bits
    return cipher

def decrypt(pk, ciphertext):
    #Decrypts the ciphertexts
    key, n = pk
    #Creates plaintext based on the ciphertext 
    #Ciphertext created using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    #Returns an array of bits
    return ''.join(plain)
    

if __name__ == '__main__':
    #print statements
    print "Extra Credit W202 Project"
    print "RSA Decrypter & Encryption Key Generator"
    p = int(raw_input("Enter a prime number (ex: 2, 3, 5, 7, 11, 13, 17,etc) : "))
    q = int(raw_input("Enter another prime number (Must be different from the previous prime entered): "))
    print "Generating public/private keypairs"
    public, private = generate_keypair(p, q)
    print "Your public key: ", public ," and your private key: ", private
    message = raw_input("Enter a message to encrypt using your private key: ")
    encrypted_msg = encrypt(private, message)
    print "Your encrypted message is: "
    print ''.join(map(lambda x: str(x), encrypted_msg))
    print "Decrypting message with your public key: ", public
    print decrypt(public, encrypted_msg)
