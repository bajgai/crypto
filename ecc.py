from unittest import TestCase
from random import randint
class FieldElement:
	def __init__(self, num, prime):
		if num >= prime or num < 0:
			error = 'Num {} not in field range 0 to {}'.format(num, prime-1)
			raise ValueError(error)
		self.num = num
		self.prime = prime

	def __repr__(self):
		return 'FieldElement_{}({})'.format(self.prime, self.num)

	def __eq__(self, other):
		if other is None:
			return False
		return self.num == other.num and self.prime == other.prime

	def __ne__(self, other):
		return not (self == other)

	def __add__(self, other):
		if self.prime != other.prime:
			raise TypeError('Cannot add two numbers in different field')
		num = (self.num + other.num) % self.prime
		return self.__class__(num, self.prime)

	def __sub__(self, other):
		if self.prime != other.prime:
			raise TypeError('Cannot substract two numbers in differen field')
		num = (self.num - other.num ) % self.prime
		return self.__class__(num, self.prime)

	def __mul__(self, other):
		if self.prime != other.prime:
			raise TypeError('Cannot multiply 2 number in different set')
		num = (self.num * other.num) % self.prime
		return self.__class__(num, self.prime)

	def __pow__(self, exponent):
		n = exponent % (self.prime -1)
		num = pow(self.num, n , self.prime)
		return self.__class__(num, self.prime)

	def __truediv__(self,other):
		if self.prime != other.prime:
			raise TypeError('Cannot divide 2 numbers in differen field')
		num = self.num * pow(other.num, self.prime-2, self.prime) % self.prime
		return self.__class__(num, self.prime)

	def __rmul__(self, coefficient):
		num = (self.num *coefficient) % self.prime
		return self.__class__(num= num, prime = self.prime)


class Point:
	def __init__(self, x, y, a, b):
		self.a = a
		self.b = b
		self.x = x
		self.y = y 
		if self.x is None and self.y is None:
			return
		if self.y**2 != self.x**3 + a * x + b:
			raise ValueError('({}, {}) is not on the curve'.format(x,y ))

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

	def __ne__(self, other):
		return not (self == other)

	def __repr__(self):
		if self.x is None:
			return 'Point(infinity)'
		elif isinstance(self.x, FieldElement):
			return 'Point({}, {})_{}_{} FieldElement({})'.format(self.x.num, self.y.num, self.a.num, self.b.num, self.x.prime)
		else:
			return 'Point({}, {})_{}_{}'.format(self.x, self.y, self.a, self.b)
	
	def __add__(self, other):
		if self.a != other.a or self.b != other.b:
			raise TypeError('Point {}, {} are not in the same curve'.format(self, other))
		if self.x is None:
			return other
		if other.x is None:
			return self

		if self.x == other.x and self.y != other.y:
			return self.__class__(None, None, self.a, self.b)

		if self.x != other.x:
			s = (other.y - self.y) / (other.x - self.x)
			x3 = s**2 - self.x - other.x
			y3 = s * (self.x - x3) - self.y
			return self.__class__(x3, y3, self.a, self.b)

		if self == other:
			s = (3 * (self.x**2) + self.a) / (2 * self.y)
			x3 = s**2 - 2  * self.x
			y3 = s * (self.x - x3) - self.y
			return self.__class__(x3, y3, self.a, self.b)

		if self == other and self.y  == 0 * self.x:
			return self.__class__(None, None, self.a, self.b)



	def __rmul__(self, coefficient):
		coef = coefficient
		current = self
		result = self.__class__(None, None, self.a, self.b)
		while coef:
			if coef & 1:
				result +=current
			current += current
			coef >>= 1
		return result

	



P = 2**256 - 2**32 - 977

class S256Field(FieldElement):
	def __init__(self, num, prime = None):
		super().__init__(num = num, prime = P)

	def __repr__(self):
		return '{:x}'.format(self.num).zfill(64)

	def sqrt(self):
		return self**((P + 1)// 4)

class S256Point(Point):
	def __init__(self, x, y, a = None, b = None):
		a, b = S256Field(A), S256Field(B)
		if type(x) == int:
			super().__init__(x = S256Field(x), y = S256Field(y), a = a, b = b)
		else:
			super().__init__(x=x, y=y, a=a, b=b)
	def __rmul__(self, coefficient):
		coef = coefficient % N
		return super().__rmul__(coef)

	def verify(self, z, sig):
		s_inv = (sig.s, N-2, N)
		u = z * s_inv % N
		v = sig.r * s_inv % N
		total = u * G + v * self
		return total.x.num == sig.r

	def sec(self, compressed=True):
		'''returns the binary version of the SEC format'''
		if compressed:
			if self.y.num % 2 == 0:
				return b'\x02' + self.x.num.to_bytes(32, 'big')
			else:
				return b'\x03' + self.x.num.to_bytes(32, 'big')
		return b'\x04' + self.x.num.to_bytes(32, 'big')+self.y.num.to_bytes(32, 'big')

	@classmethod
	def parse(self,sec_bin):
		'''returns a Point object from a SEC binary (not hex)'''
		if sec_bin[0] == 4:
			x = int.from_bytes(sec_bin[1:33], 'big')
			y = int.from_bytes(sec_bin[33:65], 'big')
			return S256Point(x = x, y =y)
		is_even = sec_bin[0] == 2
		x = S256Field(int.from_bytes(sec_bin[1:], 'big'))
		
		#right side of the equation y^2 = X^3 +7
		alpha = x**3 + S256Field(B)

		#solve for left side
		beta = alpha.sqrt()

		if beta.num % 2 == 0:
			even_beta = beta
			odd_beta = S256Field(P - beta.num)
		else:
			even_beta = S256Field(P - beta.num)
			odd_beta = beta
		if is_even:
			return S256Point(x, even_beta)
		else:
			return S256Point(x, odd_beta)


A = 0
B = 7
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
G = S256Point(
		0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
        0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)	

class PrivateKey:
	def __init__(self, secret):
		self.secret = secret
		self.point = secret * G

	def hex(self):
		return '{:x}'.format(self.secret).zfill(64)

	def sig(self, z):
		k = self.deterministic_k(z)
		r = (k*G).x.num
		k_inv = pow(k,N-2,N)
		s = (z + r * e) * k_inv % N
		if s > N/2:
			s = N - s
		return Signature(r,s)

	def deterministic_k(self, z):
		k = b'\x00'*32
		v = b'\x01'*32

		if z > N:
			z -= N
		z_bytes = z.to_bytes(32, 'big')
		secret_bytes = self.secret.to_bytes(32, 'big')
		s256 = hashlib.sha256
		k = hmac.new(k, v+'b\x00'+secret_bytes+z_bytes, s256).digest()
		v = hmac.new(k, v, s256).digest()
		k = hmac.new (k, v+'b\x01'+secret_bytes+z_bytes, s256).digest()
		v = hmac.new(k, v, s256).digest()

		while True:
			v =hmac.new(k, v, s256).digest()
			candidate = int.from_bytes(v,'big')
			if candidate >=1 and candidate < N:
				return candidate
			k = hmac.new(k, v+b'\x00', s256).digest()
			v = hmac.new(k, v, s256).digest()


class Signature:
	def __init__(self, r, s):
		self.r = r
		self.s = s

	def __rper__(self):
		return('Signature({:x},{:x})'.format(self.r,self.s))

class ECCTest(TestCase):

	def test_on_curve(self):
		prime  = 223
		a = FieldElement(0, prime)
		b = FieldElement(7, prime)
		valid_points = ((192, 105), (17, 56), (1, 193))
		invalid_points = ((200,119), (42, 99))

		for x_raw, y_raw in valid_points:
			x = FieldElement(x_raw, prime)
			y = FieldElement(y_raw, prime)
			Point(x,y,a,b)

		for x_raw, y_raw in invalid_points:
			x = FieldElement(x_raw, prime)
			y = FieldElement(y_raw, prime)
			with self.assertRaises(ValueError):
				Point(x,y,a,b)

	def test_add(self):
		prime = 223
		a = FieldElement(0, prime)
		b = FieldElement(7, prime)

		additions = (
			(192, 105, 17, 56, 170, 142),
			(170, 142, 60, 139, 220, 181),
			(47, 71, 17, 56, 215, 68),
			(143, 98, 76, 66, 47, 71))

		for x1,y1,x2,y2,x3,y3 in additions:
			p1 = Point(FieldElement(x1,prime), FieldElement(y1,prime), a, b)
			p2 = Point(FieldElement(x2, prime), FieldElement(y2, prime), a, b)
			p3 = Point(FieldElement (x3, prime), FieldElement(y3, prime), a, b)
			self.assertEqual(p1+p2, p3)






















