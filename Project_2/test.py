from OpenSSL import crypto
from Crypto.Hash import SHA256

# RSA 형식으로 2048bit 키 생성 
pkey = crypto.PKey()
pkey.generate_key(crypto.TYPE_RSA, 2048)

# Key 추출 해내기
# ASN1 형식으로 publickey를 바로 쓸 것
dump = crypto.dump_publickey(crypto.FILETYPE_ASN1, pkey)
pub_key = crypto.load_publickey(crypto.FILETYPE_ASN1, dump)
print(pub_key)

# ASN1 형식으로 privatekey를 바로 쓸 것
dump = crypto.dump_privatekey(crypto.FILETYPE_ASN1, pkey)
priv_key = crypto.load_privatekey(crypto.FILETYPE_ASN1, dump)
print(priv_key)

from Crypto.PublicKey import RSA
clientKey = RSA.generate(2048)
DATA = clientKey.publickey().export_key('DER')

# Public key를 Server의 private key로 sign한다. (Server가 전송했음을 보증)
with open("server_private.pem", 'rb+') as file:
    private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, file.read())
    #private_key = priv_key
    hashed_one = SHA256.new(DATA).digest()
    signed_one = crypto.sign(private_key, hashed_one, 'sha256')

# Server에서 public key가 인증되었는지 확인
with open("server_public.pem", 'rb+') as file:
    # 인증서를 비교하기 위한 객체들
    server_public_key = crypto.load_publickey(crypto.FILETYPE_PEM, file.read())
    #server_public_key = pub_key
    hashed_two = SHA256.new(DATA).digest()
    X509 = crypto.X509()
    X509.set_pubkey(server_public_key)

# 비교해보자
try:
    crypto.verify(X509, signed_one, hashed_two, 'sha256')
    print("됐다?")
except:
    print("아닌듯 하오")

print(len('1'.encode()))