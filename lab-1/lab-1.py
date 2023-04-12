alphabet = ["abcdefghijklmnopqrstuvwxyz",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
            "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"]
mode = [26, 26, 33, 33]


def encryption(text, key):
    result = ''
    for i in text:
        success = False
        for x in range(len(alphabet)):
            guess = alphabet[x]
            if i in guess:
                result += guess[(guess.find(i) + key) % mode[x] - 1]
                success = True
                break
        if success is not True:
            result += i
    # print(result)
    return result


def decription(text):
    print('Если хотите продолжить - нажимайте 1, для выхода - 0')
    for key in range(33):
        result = encryption(text, key)
        print('key = ', key, '\t', result)
        # flag = 0
        # print('Продолжить? ', flag=int(input()))
        flag = int(input('Продолжить? '))
        if flag == 0:
            return result


if __name__ == '__main__':
    f = open('lab-1\\text2.txt')
    text = f.read()
    print(text)
    # fk = open('key.txt', 'w+')
    # fk.write('4')
    # text_key = fk.read()
    # key = int(text_key)
    # fk.close()
    key = 31
    cipher = encryption(text, key)
    result = decription(cipher)
    f2 = open('lab-1\\result.txt', 'w')
    f2.write(result)
    f2.close()
