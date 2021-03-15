from Crypto.Cipher import DES
from Crypto import Random

class des_ECB:
    def __init__(self, key = Random.new().read(8)):
        self.key = key
        self.BS = DES.block_size
    
    # 데이터를 암호화 하여 encrypt_data를 반환하는 함수
    def encrypt(self, data):
        # 데이터를 AES 크기에 맞게 조정하기 위함
        length = len(data)
        remainder = self.BS - length % self.BS
            # remainder를 chr 변환, byte 로 바꾸어 remainder 만큼 반복
        data += chr(remainder).encode() * remainder
        # 데이터를 암호화 하기
        encryptor = DES.new(self.key, DES.MODE_ECB)
        encrypted_data = encryptor.encrypt(data)
        # data를 반환 
        return encrypted_data
    
    # 데이터를 복호화 하여 decrpyt_data를 str 형식으로 반환하는 함수
    def decrypt(self, encrypted_data):
        # 데이터를 복호화 하기
        encryptor = DES.new(self.key, DES.MODE_ECB)
        decrypted_data = encryptor.decrypt(encrypted_data)
        # 추가했던 데이터 삭제 작업 (byte -> string (크기) -> ord)
        added_size = ord(decrypted_data[-1:].decode())
        decrypted_data = decrypted_data[:-added_size]
        # data를 반환
        return decrypted_data