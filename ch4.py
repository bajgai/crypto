from ecc import PrivateKey

def ex1():
	
	P1 = PrivateKey(5000)
	print(P1.point.sec(compressed = False).hex()+'\n')

	P2 = PrivateKey(2018**5)
	print(P2.point.sec(compressed = False).hex() + '\n')

	P3 = PrivateKey(0xdeadbeef12345)
	print(P3.point.sec(compressed = False).hex())

def ex2():
	




	