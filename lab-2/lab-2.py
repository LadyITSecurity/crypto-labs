import math
import numpy as np
from scipy.special import gammaincc, erfc, hyp1f1, gammainc


def berelekamp_massey(bits):
    n = len(bits)
    b = [0 for x in bits]
    c = [0 for x in bits]
    b[0] = 1
    c[0] = 1
    L = 0
    m = -1
    N = 0
    while N < n:
        d = bits[N]
        for i in range(1, L + 1):
            d = d ^ (c[i] & bits[N - i])
        if d != 0:
            t = c[:]
            for i in range(0, n - N + m):
                c[N - m + i] = c[N - m + i] ^ b[i]
            if L <= (N / 2):
                L = N + 1 - L
                m = N
                b = t
        N = N + 1
    return L, c[0:L]


def linear_complexity_test(bits: str, patternlen=None):
    n = len(bits)
    if patternlen is not None:
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
    for i in range(K+1):
        tmp = ((v[i] - N * pi[i]) ** 2.0) / (N * pi[i])
        chisq += tmp
    P = gammainc((K / 2.0), (chisq / 2.0))
    # success = (P >= 0.01)
    return  P, None


def spectral_test(bin_data: str):
    n = len(bin_data)
    plus_minus_one = []
    for char in bin_data:
        if char == '0':
            plus_minus_one.append(-1)
        elif char == '1':
            plus_minus_one.append(1)
    s = np.fft.fft(plus_minus_one)
    modulus = np.abs(s[0:n % 2])
    tau = np.sqrt(np.log(1 / 0.05) * n)
    count_n0 = 0.95 * (n / 2)
    count_n1 = len(np.where(modulus < tau)[0])
    d = (count_n1 - count_n0) / np.sqrt(n * 0.95 * 0.05 / 4)
    p_val = erfc(abs(d) / np.sqrt(2))
    return p_val


def overlapping_patterns_test(bin_data: str, pattern_size=9, block_size=64):
    n = len(bin_data)
    pattern = ""
    for i in range(pattern_size):
        pattern += "1"
    num_blocks = math.floor(n / block_size)
    lambda_val = float(block_size - pattern_size + 1) / pow(2, pattern_size)
    eta = lambda_val / 2.0
    piks = [get_prob(i, eta) for i in range(5)]
    diff = float(np.array(piks).sum())
    piks.append(1.0 - diff)
    pattern_counts = np.zeros(6)
    for i in range(num_blocks):
        block_start = i * block_size
        block_end = block_start + block_size
        block_data = bin_data[block_start:block_end]
        pattern_count = 0
        j = 0
        while j < block_size:
            sub_block = block_data[j:j + pattern_size]
            if sub_block == pattern:
                pattern_count += 1
            j += 1
        if pattern_count <= 4:
            pattern_counts[pattern_count] += 1
        else:
            pattern_counts[5] += 1
    chi_squared = 0.0
    for i in range(len(pattern_counts)):
        chi_squared += pow(pattern_counts[i] - num_blocks * piks[i], 2.0) / (num_blocks * piks[i])
    return gammaincc(5.0 / 2.0, chi_squared / 2.0)


def get_prob(u, x):
    out = 1.0 * np.exp(-x)
    if u != 0:
        out = 1.0 * x * np.exp(2 * -x) * (2 ** -u) * hyp1f1(u + 1, 2, x)
    return out


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
    while cnt < n:
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
    while cnt < n:
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
    f = open('lab-2\\data.e')
    array_e = f.read()
    f = open('lab-2\\data.pi')
    array_pi = f.read()
    array = []
    for i in array_e:
        if i == '1' or i == '0':
            array.append(int(i))
    arrayPi = []
    for i in array_pi:
        if i == '1' or i == '0':
            arrayPi.append(int(i))

    SIZE = 100
    # first, first_str, first_period = lfsr1(SIZE)
    # second, second_str, second_period = lfsr2(SIZE)
    # third, third_str, third_period = lfsr3(SIZE)
    # result, result_str = select_generator(first, second, third)
    # print(first)
    # print(second)
    # print(third)
    # print(first_period)
    # print(second_period)
    # print(third_period)
    # print(result)
    # print('\nСтатистические тесты:')
    #
    # print('\nНа линейную сложность e')
    # success, p, _ = linear_complexity_test( array, patternlen=8)
    # print("p = ", p, '')
    #
    # print('\nСпектральный e')
    # p = spectral_test(array_e)
    # print("p = ", p, '')
    #
    # print('\nСовпадение перекрывающихся шаблонов e')
    # p = overlapping_patterns_test(array_e)
    # print("p = ", p)
    #
    # print('\nСпектральный pi')
    # p = spectral_test(array_pi)
    # print("p = ", p, '')
    #
    # print('\nСовпадение перекрывающихся шаблонов pi')
    # p = overlapping_patterns_test(array_pi)
    # print("p = ", p)
    #
    print('\nНа линейную сложность pi')
    p, _ = linear_complexity_test(arrayPi, patternlen=495)
    print("p = ", p, '')

    # test = [1,1,0,1,0,1,1,1,1,0,0,0,1]
    # success, p, _ = linear_complexity_test(test, patternlen=13)
    # print("p = ", p, '')