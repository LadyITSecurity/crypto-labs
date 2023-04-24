# crypto-labs
# lab-3           Тестирование на простоту и построение больших простых чисел.
# Вариант 5       Тест на основе малой теоремы Ферма

import random

simple_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
                  79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163,
                  167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251]


def check_small_number(number):
    for i in simple_numbers:
        if number // i != 0:
            return 0
    return 1


def __gcd(a, b):
    if b == 0:
        return a
    else:
        return __gcd(b, a % b)


def power(a, n):
    return (a ** (n - 1)) % n


def get_random(lhs, rhs=2):
    return random.randint(2, lhs)


def get_random_simple():
    index = random.randint(0, len(simple_numbers))
    return simple_numbers[index]


def test_Fermat(a, n):
    print('является ли простым число: ', n, 'проверкой деления на ', a)
    nod = __gcd(a, n)
    if nod != 1:
        print('число составное! :( \t НОД = ', nod, '\n')
        return -1
    result = power(a, n)
    print('остаток ', result)
    if result != 1:
        print('число составное! :(\n')
        return -1
    print('число простое! :)\n')
    return 0


count = 3
result = 1
while result != 0:
    n = get_random(512, 256)
    iter, result = 0, 0
    print('--------------------------------------------------------')
    while result == 0 and iter < 20:
        a = get_random_simple()
        result = test_Fermat(a, n)
        iter += 1
    a = get_random(256)
    result = test_Fermat(a, n)

