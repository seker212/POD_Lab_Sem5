def generate(e, n, x0, number_to_generate, file, loop_lock, progress):
    test_table = []
    prev = x0
    with open(file, 'w') as rngFile:
        for i in range(number_to_generate):
            if loop_lock:
                if prev in test_table:
                    return False
                else:
                    test_table.append(prev)
            prev = (prev**e) % n
            rngFile.write(bin(prev)[len(bin(prev))-1])
            progress.pop(0)
            progress.append((i+1)*100/number_to_generate)
            print(f'Progress: {progress[0]}')
        return True

def isPrime(n):
    for x in range(2,n-1):
        if n % x == 0:
            return False
    return True

def nextPrime(n):
    for i in range(n+1, 1000000000):
        if isPrime(i):
            return i

# n = 32000000
# while True:
#     n = nextPrime(n)
#     test = generate(65537, n, 131101, 1000000)
#     if test:
#         print(f'\r\n================\r\nSUCCESS: n = {n}\r\n================')