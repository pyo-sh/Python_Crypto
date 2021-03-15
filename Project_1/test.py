pathArr = [
    "cipherText_DES_ECB",
    "cipherText_DES_CBC",
    "cipherText_DES3_ECB",
    "cipherText_DES3_CBC",
    "cipherText_AES_ECB",
    "cipherText_AES_CBC",
]

for path in pathArr:
    with open(path, "rb") as textFile:
        encrypted_data = textFile.read()
        print("[%s]\n" % path)
        print(encrypted_data, "\n")