def __gcd(a, b):
	if b == 0:
		return a
	else:
		return __gcd(b, a % b)


def power(a, n):
	return (a ** (n-1)) % n


def test_Fermat(a, n):
	print('checking if a number is prime: ', n, 'with number ', a)
	if __gcd(a, n) != 1:
		print("the number isn`t prime! :(\n")
	else:
		result = power(a, n)
		print('remainder of the division ', result)
		if result != 1:
			a += 1
			test_Fermat(a, n)
		else:
			print('the number is prime! :)\n')


a = 3
n = 11
max = n + 5
while n < max:
	test_Fermat(a, n)
	n += 1

