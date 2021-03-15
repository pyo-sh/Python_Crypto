import socket
# OpenSSL 인증 방식을 사용하기 위한 모듈
from OpenSSL import crypto
from Crypto.Hash import SHA256
# RSA 암호화 방식을 사용하기 위한 모듈
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
# DES3, CBC 암호화 방식을 사용하기 위한 모듈
from DES3_CBC import des3_CBC
from Crypto import Random

def runServer(ip, port):
    # 연결하기
    #--------------------------------------------------------#
    TCPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsocket.bind((ip, port))
    print('Connection Waiting')
    TCPsocket.listen(1)
    connection, addr = TCPsocket.accept()
    print('Connected Client (ip, port)', addr)
    #--------------------------------------------------------#
    
    # 인증하기
    #--------------------------------------------------------#
    # Client에게 public key 전송 받기
    received_clientKey = connection.recv(2048)
    clientKey = RSA.import_key(received_clientKey)
    clientEncryptor = PKCS1_OAEP.new(clientKey)
    print("상대의 Public_Key를 수신했습니다.")

    # Public key를 Server의 private key로 sign한다. (Server가 전송했음을 보증)
    with open("server_private.pem", 'rb+') as file:
        private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, file.read())
        # Client Key를 Hash 및 Sign 하기
        hashed_Client_Key = SHA256.new(received_clientKey).digest()
        signed_Client_Key = crypto.sign(private_key, hashed_Client_Key, 'sha256')
        connection.sendall(signed_Client_Key)

    # 인증이 완료되었는지 확인
    if not connection.recv(1) == '1'.encode():
        exit(0)

    # 생성된 랜덤 Key를 Client의 public key로 RSA 암호화를 사용하고
    key = Random.new().read(16)
    sendKey = clientEncryptor.encrypt(key)
    connection.sendall(sendKey)
    # hashed Data에 sign하여 전송
    hashed_sendKey = SHA256.new(sendKey).digest()
    signed_sendKey = crypto.sign(private_key, hashed_sendKey, 'sha256')
    connection.sendall(signed_sendKey)
    print("Key와 Signed Key 전송완료")

    # 인증이 완료되었는지 확인
    if not connection.recv(1) == '1'.encode():
        exit(0)
    
    # 생성된 랜덤 IV를 Client의 public key로 RSA 암호화를 사용하고
    iv = Random.new().read(8)
    sendIV = clientEncryptor.encrypt(iv)
    connection.sendall(sendIV)
    # hased Data에 sign하여 전송
    hashed_sendIV = SHA256.new(sendIV).digest()
    signed_sendIV = crypto.sign(private_key, hashed_sendIV, 'sha256')
    connection.sendall(signed_sendIV)
    print("IV와 Signed IV 전송완료")

    # 인증이 완료되었는지 확인
    if not connection.recv(1) == '1'.encode():
        exit(0)
    #--------------------------------------------------------#

    # 암호화 / 복호화를 위한 객체 생성
    Encryptor = des3_CBC(key, iv)

    # ID, Password 확인하기
    # 인증을 했으므로 Server에서 보낸게 아니라면 Client에서 ID / PW 를 전송하지 않을 것
    #--------------------------------------------------------#
    print("ID / Password 인증 대기 중...")
    certified = False
    count = 0
    while count < 5:
        certification = Encryptor.decrypt(connection.recv(1024))

        with open('./pw', 'rb') as pwFile:
            line = "True"
            while line:
                line = pwFile.readline()
                if certification == line:
                    print('Authentication Complete : ' + line.decode())
                    certified = True

        if certified:
            connection.send(Encryptor.encrypt("True".encode()))
            break
        else:
            count += 1
            message = "False" if count < 5 else "close"
            connection.send(Encryptor.encrypt(message.encode()))

    if not certified:
        connection.close()
        print('Connection Break')
    #--------------------------------------------------------#


    # client 가 정수를 계속 입력할 수 있게 한다.
    #--------------------------------------------------------#
    while certified:
        # 받고 싶은 파일 이름을 수신 및 복호화
        clientCall = Encryptor.decrypt(connection.recv(1024)).decode()
        
        # 서버를 닫으라고 명령을 내릴 때 서버 OFF
        if clientCall == "close":
            connection.close()
            return

        squaredValue = int(clientCall) * int(clientCall)
        print("Client가 전송한 정수 : ", clientCall, " 제곱 값 : ", squaredValue)
        connection.send(Encryptor.encrypt(squaredValue.to_bytes(16, 'big')))
    #--------------------------------------------------------#
        


# 서버 구동을 위한 정보 저장
#ip = '192.168.22.3'
ip = '127.0.0.1'
port = 52522

# 서버 구동
runServer(ip, port)