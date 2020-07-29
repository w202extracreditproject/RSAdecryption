from random import randint
from sys import getsizeof
import math
import sage.all

def pow_mod(x,a,n):
	result = 1
	x = x % n
	while a > 0:
		if (a % 2 == 1):
			result = (result * x) % n
		a = a >> 1
		x = (x * x) % n
	return result

def is_prime(x):
	if (x % 2) == 0:
		return False
	else:
		result = pow_mod(2, x-1, x)
	
	if result == 1:
		return True
	else:
		return False

def extended_euclid(e, n):
	t = 0
	new_t = 1	
	r = n 
	new_r = e
	
	while not (new_r == 0):
		quotient = r / new_r
		t, new_t = new_t, t - quotient * new_t
		r, new_r = new_r, r - quotient * new_r
			
	if t < 0:
		t = t + n

	return t
			
def key_setup():
	p = 0;
	q = 0;
	range_start = 10**(100-1)
	range_end = (10**100)-1
	found = False
	while not found:
		num = randint(range_start, range_end)
		found = is_prime(num)
	p = num

	found = False
	while not found:
		num = randint(range_start, range_end)
		found = is_prime(num)
	q = num
	
	n = p * q
	new_n = (p-1) * (q-1)
	e = 65537
	d = extended_euclid(e, new_n)
	with open("public_key.txt", 'w') as f:
		print >> f, n,",", e 
	
	with open("private_key.txt", 'w') as f:
		print >> f, d


def key_setup_rsa():
	p = 64135289477071580278790190170577389084825014742943447208116859632024532344630238623598752668347708737661925585694639798853367;
	q = 33372027594978156556226010605355114227940760344767554666784520987023841729210037080257448673296881877565718986258036932062711;
	
	n = p * q
	phi = (p-1) * (q-1)
	e = 65537
	d = extended_euclid(e, phi)
	return ((e,n),(d,n))

def encrypt(public_key, plaintext):
	size = getsizeof(plaintext)
	e, n = public_key
	print("ORIGINAL MESSAGE: " + plaintext) 
	list_message = []
	for x in range(0, int(math.ceil(size/81.0))):
		list_message.append(plaintext[(81*x):81*(x+1)])

	
	int_message = 0
	list_int_message = []
	count = 0

	for x in range(len(list_message)):
		for y in list_message[x]:
			y = ord(y) * (256**count )
			int_message += y	
			count += 1
		list_int_message.append(int_message)
		int_message = 0 
		count = 0
			
	
	list_ciphertext = []

	for x in range(len(list_int_message)):
		ciphertext = pow_mod(list_int_message[x],e,n)
		list_ciphertext.append(ciphertext)
		
	str_ciphertext = ''
	str_ciphertext = ''.join(str(v) for v in list_ciphertext)
	print "cipher text",str_ciphertext
	return str_ciphertext
	

def decrypt(private_key, ciphertext):

	size = getsizeof(ciphertext)
	d,n = private_key
	list_cipher = []
	message = []

	list_cipher = ciphertext.split(",")

	int_message = []

	for x in range(0, len(list_cipher)):		
		int_message.append(pow_mod(int(list_cipher[x]), d, n))
		
	ascii_values = []

	for y in range(0, len(int_message)):
		for x in range(0, 81):
			message.append(int_message[y] % (256**(x + 1)))
			if x > 0:
				ascii_values.append((message[x + 81*y] - message[(x+81*y)-1])/(256**x))		
			else:
				ascii_values.append(message[x+ 81*y])

	final_message = ''
	final_message = ''.join(chr(v) for v in ascii_values)
	final_message = final_message.rstrip('\0')
	print("DECRYPTED MESSAGE: " + final_message)
	return final_message

def factorize(n):
	print sage.all.factor(n)

if __name__ == '__main__':
	#key_setup()
	public_key, private_key = key_setup_rsa()
	print "Public key:",public_key
	print "Private Key", private_key
	ciphertext = encrypt(public_key,"Hello World")
	plaintext = decrypt(private_key,ciphertext)
	print plaintext
	factorize(182191144722964401241857980467499740913)
	print "Factorization complete"
