alphabet = ["abcdefghijklmnopqrstuvwxyz",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
            "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"]
mode = [26, 26, 33, 33]


def function(text, s):
    result = ''
    for i in text:
        success = False
        for x in range(len(alphabet)):
            guess = alphabet[x]
            if i in guess:
                result += guess[(guess.find(i) + s) % mode[x] - 1]
                success = True
                break
        if success is not True:
            result += i
    print(result)
    return result


if __name__ == '__main__':
    text = 'привет, Arisa'
    s = 4
    function(text, s)
