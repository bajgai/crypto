from unittest import TestCase
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
A = 0
B = 7

class S256Point(Point):
	def __init__(self, x, y, a = None, b = None):
		a, b = S256Field(A), S256Field(B)
		if type(x) == int:
			super().__init__(x = S256Field(x), y = S256Field(y), a = a, b = b)
		else:
			super().__init__(x=x, y=y, a=a, b=b)		

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






















