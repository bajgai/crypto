from ecc import FieldElement as FE, Point as P

def ex4():
	prime = 223
	a = FE(0,prime)
	b = FE(7, prime)

	#a 2*(192, 105)
	p = P(FE(192,prime), FE(105, prime), a, b)
	print("2 * (192, 105) is:  {}".format(p+p))
    
    #b 2*(143, 98)
	p = P(FE(143,prime), FE(98, prime), a, b)
	print("2 * (143, 98) is : {}".format(p+p))

	#c 2*(47, 71)
	p = P(FE(47, prime), FE(71, prime), a, b)
	print("2 * (47,71) is : {}".format(p+p))

	#d 4*(47, 71)
	print("4 * (47, 71) is : {}".format(p+p+p+p))

	#e 8*(47, 71)
	ans = p
	for i in range(7):
		ans += p
	print ("8 * (47, 71) is : {}".format(ans))

	#f 21*(47,71)
	ans = p
	for i in range(20):
		ans += p
	print ("21*(47,71) is : {}".format(ans))
	
