import re

def single_bits_test(file_path):
    with open(file_path, 'r') as file:
        n = len(re.findall("1", file.read(20000)))
    if n > 9725 and n < 10275:
        return True
    else:
        return False


def series_test(file_path):
    test_dict = {
        1: [2315, 2685],
        2: [1114, 1386],
        3: [527, 723],
        4: [240, 384],
        5: [103, 209],
        6: [103, 209],
    }
    with open(file_path, 'r') as file:
        text = file.read(20000)
        coma = ""
        for i in range(1,7):
            if i == 6:
                coma = ','
            else:
                coma = ''
            for j in range(2):
                if j == 0:
                    regexString = "(?=((^|1)0{" + str(i) + coma + "}(1|$)))"     # r"(?=((^|1)0{1}(1|$)))"
                elif j == 1:
                    regexString = "(?=((^|0)1{" + str(i) + coma + "}(0|$)))"
                else:
                    raise Exception("Not supported exception")
                regex = re.compile(regexString)
                series_count = len(re.findall(regex, text))
                if not (series_count >= test_dict[i][0] and series_count <= test_dict[i][1]):
                    return False
                # print(f"j: {j}\ti:{i}\tcount:{series_count}")
        return True
                

def long_series_test(file_path):
    with open(file_path, 'r') as file:
        if re.search(r"(0{26})|(1{26})", file.read(20000)) is None:
            return True
        else:
            return False

def poker_test(file_path):
    s = {format(i, '#06b')[2:]: 0 for i in range(16)}
    with open(file_path, 'r') as file:
        for i in range(5000):
            strNum = file.read(4)
            s[strNum] = s[strNum]+1
    sSum = 0
    for value in s.values():
        sSum += value**2
    X = 16/5000*sSum-5000
    if X > 2.16 and X < 46.17:
        return True
    else:
        return False