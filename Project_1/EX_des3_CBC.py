from Crypto.Cipher import DES3
from Crypto import Random

def _make_des3_encryptor(key, iv):
    encryptor = DES3.new(key, DES3.MODE_CBC, iv)
    return encryptor

def des3_encrypt(key, iv, data):
    encryptor = _make_des3_encryptor(key, iv)
    pad_len = 8 - len(data) % 8
    padding = chr(pad_len) * pad_len
    data += padding
    return encryptor.encrypt(data)

def des3_decrypt(key, iv, data):
    encryptor = _make_des3_encryptor(key, iv)
    result = encryptor.decrypt(data)

    pad_len = ord(result[-1:])
    print(pad_len)
    result = result[:-pad_len]
    return result

plaintext = 'This is a plain text123'
ciphertext = ''
key = b'Sixteen byte key'
BS = DES3.block_size
iv = Random.new().read(BS)
ciphertext = des3_encrypt(key, iv, plaintext)
print(ciphertext)

dectext = des3_decrypt(key, iv, ciphertext)
print(dectext)