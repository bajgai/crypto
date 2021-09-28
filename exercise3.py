from ecc import FieldElement as FE, Point as P

def exercise3_4():
	prime = 223
	a = FE(0,prime)
	b = FE(7, prime)

	#a 2*(192, 105)
	p = P(FE(192,prime), FE(105, prime), a, b)
	print("2 * (192, 105) is:  {}".format(p+p))