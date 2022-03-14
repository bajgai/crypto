from ecc import PrivateKey
from ecc import Signature

def ex1():
	
	P1 = PrivateKey(5000)
	print(P1.point.sec(compressed = False).hex()+'\n')

	P2 = PrivateKey(2018**5)
	print(P2.point.sec(compressed = False).hex() + '\n')

	P3 = PrivateKey(0xdeadbeef12345)
	print(P3.point.sec(compressed = False).hex())

## Find the compressed SEC format for the public key where the private key secrets are:

def ex2():
	P1 = PrivateKey(5001)
	print(P1.point.sec(compressed = True).hex()+ '\n')

	P2 = PrivateKey(2019 **5)
	print(P2.point.sec(compressed = True).hex() + '\n')

	P3 = PrivateKey(0xdeadbeef54321)
	print(P3.point.sec(compressed = True).hex())

def ex3():
	r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
	s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
	sig = Signature(r,s)
	print(sig.der().hex())
	




	