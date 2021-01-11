def nwd(a, b):
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a

def isPrime(n):
    for x in range(2,n-1):
        if n % x == 0:
            return False
    return True

def coprime(n): # return e
    i = 2
    while not (nwd(i,n) == 1 and isPrime(i)):
        i += 1
    return i

def genD(e,phi): #return d
    d = 1
    while (e*d-1) % phi != 0:
        d += 1
    return d

def gen(p, q): #return n, phi
    n = p * q
    phi = (p-1)*(q-1)
    return n,phi 

def saveKey(a, b, filePath):
    with open(filePath, 'w') as f:
        f.write(str(a) + '\n' + str(b))

def readKey(filePath):
    a = None
    b = None
    with open(filePath, 'r') as f:
        a = f.readline()
        b = f.readline()
        return a, b

def genKeys(p, q): # returns e, d, n
    n, phi = gen(p, q)
    e = coprime(phi)
    d = genD(e, phi)
    return e, d, n

def encrypt(inputFilePath, keyFilePath, outputFilePath):
    with open(inputFilePath, 'rb') as inputFile:
        test = inputFile.read()
        test2 = test.decode('UTF-8', 'ignore')
        mTable = [ord(letter) for letter in test2]
    e, n = readKey(keyFilePath)
    e = int(e)
    n = int(n)
    if any(m > n for m in mTable):
        raise ValueError("n value is too small")
    outputTextTable = [(m**e)%n for m in mTable]
    with open(outputFilePath, 'w') as outputFile:
        for x in outputTextTable:
            outputFile.write(str(x) + ' ')
        

def decrypt(inputFilePath, keyFilePath, outputFilePath):
    mTable = None
    with open(inputFilePath, 'r') as inputFile:
        test = inputFile.read()
        mTable = test.split()
        for i in range(len(mTable)):
            mTable[i] = int(mTable[i])
    e, n = readKey(keyFilePath)
    e = int(e)
    n = int(n)
    outputTextTable = [chr((m**e)%n) for m in mTable]
    with open(outputFilePath, 'wb') as outputFile:
        outputFile.write(''.join(outputTextTable).encode('UTF-8', 'ignore'))

if __name__ == "__main__":
    e, d, n = genKeys(31, 19)
    saveKey(e,n,'key_pub.txt')
    saveKey(d,n,'key_prv.txt')
    encrypt('in.txt', 'key_pub.txt', 'out.txt')
    decrypt('out.txt', 'key_prv.txt', 'out2.txt')