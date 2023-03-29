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
    key = 0
    for i in range(33):
        result = encryption(text, key)
        print(key, '\t', result)


if __name__ == '__main__':
    text = 'привет, Arisa'
    key = 4
    decription(text)
