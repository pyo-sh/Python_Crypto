from OpenSSL import crypto
from Crypto.Hash import SHA256

# RSA 형식으로 2048bit 키 생성 
pkey = crypto.PKey()
pkey.generate_key(crypto.TYPE_RSA, 2048)

# Key 추출 해내기
# PEM 형식으로 publickey를 파일로 저장 (배포되었다고 가정)
with open("server_public.pem", 'ab+') as file:
    file.write(crypto.dump_publickey(crypto.FILETYPE_PEM, pkey))
    
# PEM 형식으로 privatekey를 파일로 저장 (서버만 이를 가지고 있다고 가정)
with open("server_private.pem", 'ab+') as file:
    file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))