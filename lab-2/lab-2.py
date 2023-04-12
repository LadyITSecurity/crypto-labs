def lfsr1(n):
    flag = 0
    period = 0
    cnt = 0
    start_state = 0b1101001
    state = 0b11101001
    lst = list()
    lst.append(state & 1)
    while (cnt < n):
        newbit = ((state >> 7) ^ (state >> 1) ^ state) & 1
        state = (state >> 1) | (newbit << 6)
        lst.append(state & 1)
        cnt += 1
        if start_state == state and flag == 0:
            flag = 1
            period = cnt
    string = "".join(map(str, lst))
    return lst, string, period



if __name__ == '__main__':
    SIZE = 100
    first, first_str, first_period = lfsr1(SIZE)
    print(first)
