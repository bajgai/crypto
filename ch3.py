import ecc


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

def ex6():
	# Verify the signatures
	P = (0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c,
         0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34)

	# signature 1
	z = 0xec208baa0fc1c19f708a9ca96fdeff3ac3f230bb4a7ba4aede4942ad003c0f60
	r = 0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395
	s = 0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4
	point = ecc.S256Point(P[0], P[1])
	s_inv = pow(s, ecc.N-2, ecc.N)
	u = z * s_inv % ecc.N
	v = r * s_inv % ecc.N
	print((u * ecc.G + v*point).x.num == r)

	# signature 2
	z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
	r = 0xeff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c
	s = 0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6

	point = ecc.S256Point(P[0], P[1])
	s_inv = pow(s, ecc.N-2, ecc.N)
	u = z * s_inv % ecc.N
	v = r * s_inv % ecc.N

	print((u * ecc.G + v * point).x.num == r)