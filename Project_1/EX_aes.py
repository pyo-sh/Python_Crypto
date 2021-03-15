from Crypto.Cipher import AES
from Crypto import Random

BS = AES.block_size

def pad(m):
    return m + bytes([BS - len(m) % BS] * (BS - len(m) % BS))

def unpad(m):
    return m[:-int(m[-1])]

class AEScipher:
    def __init__(self, s_key):
        self.s_key = s_key

    def encrypt(self, plain):
        plain = pad(plain.encode())
        iv = Random.new().read(BS)
        cipher = AES.new(self.s_key, AES.MODE_CBC, iv)
        return (iv + cipher.encrypt(plain))

    def decrypt(self, e):
        iv = e[:BS]
        cipher = AES.new(self.s_key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(e[BS:])).decode()
    
aes = AEScipher(Random.new().read(32))

m = "Hello, This is an AES test abcdefg 12345 "
e = aes.encrypt(m)
d = aes.decrypt(e)

print(e)
print(d)