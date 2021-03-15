from Crypto import Random
from AES_CBC import aes_CBC
from AES_CBC import block_size

fileType = "AES_CBC"
# 같은 key, iv를 가진 다른 객체가 암호화/복호화 할 것
# 암호화/복호화 할 때 사용할 key 선언
key = Random.new().read(32)
# 암호화/복호화 할 때 사용할 iv 선언
iv = Random.new().read(block_size)
# DES 형식의 암호화를 사용할 수 있게 만든 class 객체 선언
Encryptor = aes_CBC(key, iv)

# 100 byte 크기의 text 파일을 받기
    # 파일 열어서 데이터 받기 (str 을 받을 것이므로 "r" 형식)
path = "100byte.txt"
textfile = open(path, "r")
    # 여러 줄의 str을 배열로 받아 한 str로 만드는 작업
data = "".join(textfile.readlines())
    # 파일은 닫아주기
textfile.close()
    # data 확인
print("[data]\n", data)

# class 객체를 이용해 데이터 암호화 하기
encrypted_data = Encryptor.encrypt(data.encode())
    # 결과물 print
print("\n[encrypted_data]\n", encrypted_data)

# 암호화 한 데이터를 파일에 저장하기
    # 파일을 열어서 적기 (byte 형식으로 저장할 것이므로 "wb" 형식)
path = "cipherText_" + fileType
textfile = open(path, "wb")
    # 데이터 Write
textfile.write(encrypted_data)
    # 파일은 닫아주기
textfile.close()

# 암호화 된 데이터를 저장한 파일 열기
    # 파일을 열어서 읽기 (byte 형식의 파일을 읽으므로 "rb" 형식)
textfile = open(path, "rb")
    # 암호화 된 파일 가져오기
encrypted_data = textfile.read()
    # 파일은 닫아주기
textfile.close()

# class 객체를 이용해 읽은 데이터를 복호화 하기
    # 같은 key를 이용해 DES 형식의 복호화를 사용할 수 있게 만든 class 객체 선언
Decryptor = aes_CBC(key, iv)
    # 데이터 복호화 하기
decrypted_data = Decryptor.decrypt(encrypted_data)
decrypted_data = decrypted_data.decode()
    # 결과물 print
print("\n[decrypted_data]\n", decrypted_data)