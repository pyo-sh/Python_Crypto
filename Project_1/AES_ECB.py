# 통신 데이터에 대한 암호화 / 복호화를 위한 class
from Crypto.Cipher import AES
from Crypto import Random

class aes_ECB:
    def __init__(self, key = Random.new().read(32)):
        self.key = key
        self.BS = AES.block_size
    # 데이터를 암호화 하는 함수
    # 데이터는 byte 로 받는다.
    def encrypt(self, data):
        # 데이터를 AES 크기에 맞게 조정하기 위함
        length = len(data)
        remainder = self.BS - length % self.BS
            # remainder를 chr 변환, byte 로 바꾸어 remainder 만큼 반복
        data += chr(remainder).encode() * remainder
        # 데이터를 암호화
        encryptor = AES.new(self.key, AES.MODE_ECB)
        encrypted_data = encryptor.encrypt(data)
        # 암호화 된 데이터를 반환
        return encrypted_data

    # 데이터를 복호화 하는 함수
    def decrypt(self, encrypted_data):
        # 데이터 복호화
        encryptor = AES.new(self.key, AES.MODE_ECB)
        decrypted_data = encryptor.decrypt(encrypted_data)
        # 추가했던 데이터 삭제 작업 (byte -> string -> ord)
        added_size = ord(decrypted_data[-1:].decode())
        decrypted_data = decrypted_data[:-added_size]
        # 복호화 된 데이터를 반환
        return decrypted_data