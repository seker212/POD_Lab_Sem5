from random import shuffle

class Encryption():
    def __init__(self, key = {}, maxRange = 0x11000):
        super().__init__()
        self.key = key
        self.maxRange = maxRange

    def encrypt(self, text):
        encrypted = ''
        for char in text:
            encrypted += self.key[ord(char)]
        return encrypted

    def setKey(self, password):
        if len(set(password)) != len(password):
            raise ValueError("Password doesn't consist only of unique characters")
        for i in range(len(password)):
            self.key[i] = password[i]
 
        l = 0
        for i in range(self.maxRange):
            if chr(i) not in password:
               self.key[i+len(password)-l] = chr(i)
            else:
                l += 1
    
    def generateKey(self):
        initList = [chr(i) for i in range(self.maxRange)]
        shuffle(initList)
        key = ''.join(initList)
        key = key.encode('UTF-32', 'ignore').decode('UTF-32')
        return key

# e = Encryption()
# print(e.generateKey())
# e.getKey('Aoz')
# print(e.encrypt('inputzA'))