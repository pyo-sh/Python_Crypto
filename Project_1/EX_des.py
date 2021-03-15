from Crypto.Cipher import DES

cipher = DES.new("8bytekey".encode(), DES.MODE_ECB)
encrypted_data = cipher.encrypt("0123data".encode())
print(encrypted_data)

print(cipher.decrypt(encrypted_data))
