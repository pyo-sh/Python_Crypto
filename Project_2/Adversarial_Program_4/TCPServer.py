import socket
# RSA 암호화 방식을 사용하기 위한 모듈
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
# DES3, CBC 암호화 방식을 사용하기 위한 모듈
from DES3_CBC import des3_CBC
from Crypto import Random

def runServer(ip, port):
    # 연결하기
    #--------------------------------------------------------#
    # TCP 통신을 하기 위한 객체를 생성
    TCPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 지정받은 ip와 port를 통해 통신을 시도 
    TCPsocket.bind((ip, port))
    # client 와 연결될 때 까지 대기
    print('Connection Waiting')
    TCPsocket.listen(1)
    # client와 연결 후 connection 저장
    connection, addr = TCPsocket.accept()
    print('Connected Client (ip, port)', addr)
    #--------------------------------------------------------#
    
    # RSA 으로 통신하기 위함
    # Client에게 public key 전송 받기
    clientKey = RSA.import_key(connection.recv(2048))
    clientEncryptor = PKCS1_OAEP.new(clientKey)
    print("상대의 Public_Key를 수신했습니다. 암호화 된 Key / iv 송신중...")

    # Server의 Key 생성 및 전달
    key = Random.new().read(16)
    connection.sendall(clientEncryptor.encrypt(key))
    print("Key 송신 완료")

    # Server의 iv 생성 및 전달
    iv = Random.new().read(8)
    connection.sendall(clientEncryptor.encrypt(iv))
    print("iv 송신 완료")

    # 암호화 / 복호화를 위한 객체 생성
    Encryptor = des3_CBC(key, iv)

    # ID, Password 확인하기
    print("ID / Password 인증 대기 중...")
    #--------------------------------------------------------#
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
    #--------------------------------------------------------#

    if not certified:
        connection.close()
        print('Connection Break')

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