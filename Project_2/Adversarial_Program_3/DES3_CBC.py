from Crypto.Cipher import DES3
from Crypto import Random

block_size = DES3.block_size
class des3_CBC:
    def __init__(self, key = Random.new().read(16), iv = Random.new().read(block_size)):
        self.key = key
        self.iv = iv
        self.BS = block_size

    def encrypt(self, data):
        # 데이터를 AES 크기에 맞게 조정하기 위함
        length = len(data)
        remainder = self.BS - length % self.BS
            # remainder를 chr 변환, byte 로 바꾸어 remainder 만큼 반복
        data += chr(remainder).encode() * remainder
        # 데이터를 암호화 하기
        encryptor = DES3.new(self.key, DES3.MODE_CBC, self.iv)
        encrypted_data = encryptor.encrypt(data)
        # data를 반환
        return encrypted_data

    def decrypt(self, encrypted_data):
        # 데이터를 복호화 하기
        encryptor = DES3.new(self.key, DES3.MODE_CBC, self.iv)
        decrypted_data = encryptor.decrypt(encrypted_data)
        # 추가했던 데이터 삭제 작업 (byte -> string (크기) -> ord)
        added_size = ord(decrypted_data[-1:].decode())
        decrypted_data = decrypted_data[:-added_size]
        # 데이터 반환
        return decrypted_data