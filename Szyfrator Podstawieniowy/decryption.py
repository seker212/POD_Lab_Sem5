class Decryption():
    def __init__(self, key = {}, maxRange = 0x11000):
        super().__init__()
        self.key = key
        self.maxRange = maxRange
    
    def decrypt(self, text):
        decrypted = ''
        for char in text:
            decrypted += chr(self.key[char])

        return decrypted

    def setKey(self, password):
        if len(set(password)) != len(password):
            raise ValueError("Password doesn't consist only of unique characters")
        for i in range(len(password)):
            self.key[password[i]] = i
        
        l=0
        for i in range(self.maxRange):
            if chr(i) not in password:
                self.key[chr(i)] = i+len(password)-l
            else:
                l += 1

# d = Decryption()
# d.getKey('Aoz')
# print(d.decrypt('glntsy>'))