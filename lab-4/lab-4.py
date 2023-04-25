# crypto-labs
# lab-4           Шифрование с открытым ключом
# Вариант 7       Merkle-Hellman (многократное шифрование)
import random

n = 5


def __gcd(a, b):
    if b == 0:
        return a
    else:
        return __gcd(b, a % b)


def superincreasing_sequence(n):
    b = []
    for i in range(n):
        b.append(1 + sum(b))
    return b


def get_key(n):
    b = superincreasing_sequence(n)     # 3
    m = sum(b) + 2
    w = 0                               # 4
    while True:
        w = random.randint(1, m - 1)
        if __gcd(w, m) == 1:
            break
    pi = []                             # 5
    tmp = [i for i in range(n)]
    while len(tmp) > 0:
        ind = random.randint(0, len(tmp) - 1)
        pi.append(tmp[ind])
        tmp.pop(ind)
    a = []
    for i in range(n):
        a.append(w*b[pi[i]])
    # a = [w*b[pi[i]] for i in range(n)]  # 7 - открытый ключ
    print(a)
    k = []
    for i in range(len(pi)):
        k.append(pi[i])
    # [k.append(pi[i]) for i in range(len(pi))]
    k.append(m)
    k.append(w)
    [k.append(b[i]) for i in range(len(b))]

    print(k)



if __name__ == '__main__':
    get_key(n)
