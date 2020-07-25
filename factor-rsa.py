from random import randint
from sys import getsizeof
import math
import sage.all
import time

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
			
def generateN(bits):
	p = 0;
	q = 0;
	b = bits//2
	range_start = 2**(b-1)
	range_end = (2**b)-1
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
	return n


def factorize(n):
	print ""
	print ""
	print "********* Factoring number ********* ",n
	start_time = time.time()
	f = sage.all.factor(n)
	t = (time.time() - start_time)
	print "Time taken= "'\033[94m',t, "seconds "'\033[0m'", factors = ", f
	#print("********* Factoring time --- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
	bitsForN= [32, 64, 128]
	numbers= list()
	print "*********  Generate Numbers  ********"
	for b in bitsForN:
		n = generateN(b)
		numbers.append(n)
		print "", b, "bit Number = ",n
	
	print ""
	print ""
	print "*********  Start factoring Numbers  ********"
	for n in numbers:
		factorize(n)

	print ""
	print "### Factorization complete ###"
