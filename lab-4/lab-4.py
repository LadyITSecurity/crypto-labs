# crypto-labs
# lab-4           Шифрование с открытым ключом
# Вариант 7       Merkle-Hellman (многократное шифрование)
import random

n = 5
t = 4


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


def task_superincreasing_sequence(b, s):
    x = [0] * n
    i = n - 1
    while i >= 0:
        if s >= b[i]:
            x[i] = 1
            s = s - b[i]
        else:
            x[i] = 0
        i -= 1
    return x


def get_binary(m):
    bin = []
    while m > 0:
        bin.append(m % 2)
        m = m // 2
    result = [0]*n
    while len(bin) > n:
        bin.pop(-1)
    for i in range(len(bin)):
        result[n-i-1] = bin[i]
    result[0] = 1
    result[-1] = 1
    return result


def get_key(n):
    b = superincreasing_sequence(n)  # 3
    M = sum(b) + n
    w = 0  # 4
    while True:
        w = random.randint(1, M - 1)
        if __gcd(w, M) == 1:
            break
    pi = []  # 5
    tmp = [i for i in range(n)]
    while len(tmp) > 0:
        ind = random.randint(0, len(tmp) - 1)
        pi.append(tmp[ind])
        tmp.pop(ind)
    a = []
    for i in range(n):
        a.append(w * b[pi[i]])
    # a = [w*b[pi[i]] for i in range(n)]  # 7 - открытый ключ
    k = []
    for i in range(len(pi)):
        k.append(pi[i])
    k.append(M)
    k.append(w)
    [k.append(b[i]) for i in range(len(b))]
    return a, k


def encryption(m, mode=get_key):
    a, k = mode(n)
    m = get_binary(m)
    c = 0
    for i in range(len(a)):
        c += m[i] * a[i]
    return c, k, a


def decryption(c, k):
    pi = k[:n:]
    M = k[n]
    w = k[n + 1]
    b = k[n + 2::]
    d = (w ** (M - 1) * c) % M
    r = task_superincreasing_sequence(b, d)
    m = ''
    for i in range(n):
        m += str(r[pi[i]])
    return int(m)


def get_key_mn(n):
    a = [[0] * n]
    a = [superincreasing_sequence(n)]
    M = [0] * (t + 1)
    W = [0] * (t + 1)
    for i in range(1, t + 1):
        a.append([0] * n)
        M[i] = sum(a[i - 1]) + n
        while True:
            W[i] = random.randint(1, M[i] - 1)
            if __gcd(W[i], M[i]) == 1:
                break
        for k in range(len(a[i - 1])):
            a[i][k] = (a[i - 1][k] * W[i]) % M[i]
    M.pop(0)
    W.pop(0)
    pi = []  # 5
    tmp = [i for i in range(n)]
    while len(tmp) > 0:
        ind = random.randint(0, len(tmp) - 1)
        pi.append(tmp[ind])
        tmp.pop(ind)
    k = []
    for i in range(len(pi)):
        k.append(pi[i])
    for i in range(len(M)):
        k.append(M[i])
    for i in range(len(W)):
        k.append(W[i])
    for i in range(len(a[0])):
        k.append(a[0][i])

    pi = []
    tmp = [i for i in range(n)]
    while len(tmp) > 0:
        ind = random.randint(0, len(tmp) - 1)
        pi.append(tmp[ind])
        tmp.pop(ind)
    b = []
    for i in range(n):
        b.append(a[t][pi[i]])

    return b, k


def decryption_mn(c, k):
    pi = k[:n:]
    M = k[n:n + t]
    W = k[n + t:n + 2 * t]
    b = k[n + 2 * t::]
    d = [0] * (t + 1)
    d[-1] = c
    i = len(W)-1
    while i >= 0:
        tmp = pow(W[i], M[i] - 1, M[i])
        res = (tmp * d[i+1]) % M[i]
        d[i] = res
        i -= 1
    r = task_superincreasing_sequence(b, d[0])
    m = ''
    for i in range(n):
        m += str(r[pi[i]])
    return int(m)


if __name__ == '__main__':
    m = 64
    c, k, a = encryption(m, get_key_mn)
    print('Исходное сообщение:', m)
    print('Шифруемое сообщение m:', get_binary(m))
    print('Зашифрованное сообщение с:', c)
    print('Закрытый ключ k:', k)
    print('Открытый ключ a:', a)
    m_result = decryption_mn(c, k)
    print('Дешифрованное сообщение m:', m_result)

    print('\n')
    c, k, a = encryption(m)
    print('Исходное сообщение:', m)
    print('Шифруемое сообщение m:', get_binary(m))
    print('Зашифрованное сообщение с:', c)
    print('Закрытый ключ k:', k)
    print('Открытый ключ a:', a)
    m_result = decryption(c, k)
    print('Дешифрованное сообщение m:', m_result)
