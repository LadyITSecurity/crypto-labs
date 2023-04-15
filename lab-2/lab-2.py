import math
import numpy as np
from scipy.special import gammaincc, erfc


def berelekamp_massey(bits):
    n = len(bits)
    b = [0 for x in bits]
    c = [0 for x in bits]
    b[0] = 1
    c[0] = 1
    L = 0
    m = -1
    N = 0
    while (N < n):
        d = bits[N]
        for i in range(1, L + 1):
            d = d ^ (c[i] & bits[N - i])
        if (d != 0):
            t = c[:]
            for i in range(0, n - N + m):
                c[N - m + i] = c[N - m + i] ^ b[i]
            if (L <= (N / 2)):
                L = N + 1 - L
                m = N
                b = t
        N = N + 1
    return L, c[0:L]


def linear_complexity_test(bits, patternlen=None):
    n = len(bits)
    if patternlen != None:
        M = patternlen
    else:
        if n < 1000000:
            print("Error. Need at least 10^6 bits")
            # exit()
            return False, 0.0, None
        M = 512
    K = 6
    N = int(math.floor(n / M))
    LC = list()
    for i in range(N):
        x = bits[(i * M):((i + 1) * M)]
        LC.append(berelekamp_massey(x)[0])
    a = float(M) / 2.0
    b = (((-1) ** (M + 1)) + 9.0) / 36.0
    c = ((M / 3.0) + (2.0 / 9.0)) / (2 ** M)
    mu = a + b - c
    T = list()
    for i in range(N):
        x = ((-1.0) ** M) * (LC[i] - mu) + (2.0 / 9.0)
        T.append(x)
    v = [0, 0, 0, 0, 0, 0, 0]
    for t in T:
        if t <= -2.5:
            v[0] += 1
        elif t <= -1.5:
            v[1] += 1
        elif t <= -0.5:
            v[2] += 1
        elif t <= 0.5:
            v[3] += 1
        elif t <= 1.5:
            v[4] += 1
        elif t <= 2.5:
            v[5] += 1
        else:
            v[6] += 1
    pi = [0.010417, 0.03125, 0.125, 0.5, 0.25, 0.0625, 0.020833]
    chisq = 0.0
    for i in range(K + 1):
        chisq += ((v[i] - (N * pi[i])) ** 2.0) / (N * pi[i])
    P = gammaincc((K / 2.0), (chisq / 2.0))
    success = (P >= 0.01)
    return success, P, None


def spectral(bin_data: str):

    n = len(bin_data)
    plus_minus_one = []
    for char in bin_data:
        if char == '0':
            plus_minus_one.append(-1)
        elif char == '1':
            plus_minus_one.append(1)
    s = np.fft.fft(plus_minus_one)
    modulus = np.abs(s[0:n // 2])
    tau = np.sqrt(np.log(1 / 0.05) * n)
    count_n0 = 0.95 * (n / 2)
    count_n1 = len(np.where(modulus < tau)[0])
    d = (count_n1 - count_n0) / np.sqrt(n * 0.95 * 0.05 / 4)
    p_val = erfc(abs(d) / np.sqrt(2))
    return p_val


def lfsr1(n):
    flag = 0
    period = 0
    cnt = 0
    start_state = 0b1101001
    state = 0b11101001
    lst = list()
    lst.append(state & 1)
    while cnt < n:
        newbit = ((state >> 7) ^ (state >> 1) ^ state) & 1
        state = (state >> 1) | (newbit << 6)
        lst.append(state & 1)
        cnt += 1
        if start_state == state and flag == 0:
            flag = 1
            period = cnt
    string = "".join(map(str, lst))
    return lst, string, period


def lfsr2(n):
    flag = 0
    period = 0
    cnt = 0
    start_state = 0b11111111
    state = 0b11111111
    lst = list()
    lst.append(state & 1)
    while (cnt < n):
        newbit = ((state >> 7) ^ (state >> 5) ^ (state >> 3) ^ state) & 1
        state = (state >> 1) | (newbit << 6)
        lst.append(state & 1)
        cnt += 1
        if start_state == state and flag == 0:
            flag = 1
            period = cnt
    string = "".join(map(str, lst))
    return lst, string, period


def lfsr3(n):
    flag = 0
    period = 0
    cnt = 0
    start_state = 0b00101001
    state = 0b00101001
    lst = list()
    lst.append(state & 1)
    while (cnt < n):
        newbit = ((state >> 7) ^ (state >> 5) ^ (state >> 1) ^ state) & 1
        state = (state >> 1) | (newbit << 6)
        lst.append(state & 1)
        cnt += 1
        if start_state == state and flag == 0:
            flag = 1
            period = cnt
    string = "".join(map(str, lst))
    return lst, string, period


def select_generator(first, second, third):
    lst = list()
    for j in range(0, len(first)):
        if first[j] == 0:
            lst.append(second[j])
        else:
            lst.append(third[j])
    string = "".join(map(str, lst))
    return lst, string


if __name__ == '__main__':
    SIZE = 100
    first, first_str, first_period = lfsr1(SIZE)
    second, second_str, second_period = lfsr2(SIZE)
    third, third_str, third_period = lfsr3(SIZE)
    result , result_str = select_generator(first, second, third)
    print(first)
    print(second)
    print(third)
    print(result)
    print('Статистические тесты:\n')
    print('На линейную сложность\n')
    success, p, _ = linear_complexity_test(result, patternlen=7)
    print("p = ", round(p, 3), '\n')
    print('Спектральный\n')
    p = spectral(result_str)
    print("p = ", p)

