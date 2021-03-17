import socket
# OpenSSL 인증 방식을 사용하기 위한 모듈
from OpenSSL import crypto
from Crypto.Hash import SHA256
# RSA 암호화 방식을 사용하기 위한 모듈
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
# DES3, CBC 암호화 방식을 사용하기 위한 불러오기
from DES3_CBC import des3_CBC

def runClient(ip, port):
    # 연결하기
    #--------------------------------------------------------#
    # TCP 통신을 하기 위한 객체를 생성
    TCPsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 서버와 통신이 가능하게 될 때 까지 대기
    print('Waiting for Server...')
    if not TCPsocket.connect((ip, port)):
        print('Connected to File Server!')
    #--------------------------------------------------------#

    # 인증하기
    #--------------------------------------------------------#
    # RSA 으로 통신하기 위함
    # Server에게 public key 생성 및 전달
    clientKey = RSA.generate(2048)
    send_Client_Key = clientKey.publickey().export_key('DER')
    TCPsocket.sendall(send_Client_Key)
    clientEncryptor = PKCS1_OAEP.new(clientKey)
    print("Public_Key 송신 완료")
    
    # Server에서 public key가 인증되었는지 확인
    with open("server_public.pem", 'rb+') as file:
        # 인증서를 비교하기 위한 객체들
        server_public_key = crypto.load_publickey(crypto.FILETYPE_PEM, file.read())
        X509 = crypto.X509()
        X509.set_pubkey(server_public_key)

        # Hash 된 값이 Signed 되었는지 확인
        hashed_Client_Key = SHA256.new(send_Client_Key).digest()
        received_Client_Key = TCPsocket.recv(2048)
        try:
            crypto.verify(X509, received_Client_Key, hashed_Client_Key, 'sha256')
            print("서버 인증 완료")
            TCPsocket.send('1'.encode())
        except:
            TCPsocket.send('0'.encode())
            print("ERROR! 서버 인증이 아닙니다.")
            exit(1)

    # Server의 Key 전송 받기
    received_key = TCPsocket.recv(1024)
    key = clientEncryptor.decrypt(received_key)
    # Key 인증하기
    hashed_key = SHA256.new(received_key).digest()
    signed_key = TCPsocket.recv(1024)
    try:
        crypto.verify(X509, signed_key, hashed_key, 'sha256')
        print("Key 수신 및 인증 완료")
        TCPsocket.send('1'.encode())
    except:
        TCPsocket.send('0'.encode())
        print("ERROR! Key가 서버 인증이 아닙니다.")
        exit(1)

    # Server의 iv 전송받기
    received_iv = TCPsocket.recv(1024)
    iv = clientEncryptor.decrypt(received_iv)
    # iv 인증하기
    hashed_iv = SHA256.new(received_iv).digest()
    signed_iv = TCPsocket.recv(1024)
    try:
        crypto.verify(X509, signed_iv, hashed_iv, 'sha256')
        print("IV 수신 및 인증 완료")
        TCPsocket.send('1'.encode())
    except:
        TCPsocket.send('0'.encode())
        print("ERROR! IV가 서버 인증이 아닙니다.")
        exit(1)

    # 암호화 / 복호화를 위한 encryptor class 객체 생성
    Encryptor = des3_CBC(key, iv)

    # 인증
    #--------------------------------------------------------#
    certified = False
    while not certified:
        print("[ID Password]를 입력해주세요")
        # 입력 받고 이를 암호화
        getAuthentication = Encryptor.encrypt(input().encode())
        TCPsocket.sendall(getAuthentication)

        receivedData = Encryptor.decrypt(TCPsocket.recv(1024))
        # 받은 값을 복호화 (맞는 지 틀리는 지)
        if receivedData.decode() == "True":
            certified = True
            print('Authentication Complete')
        elif receivedData.decode() == "False":
            print('Authentication Failed')
        else:
            TCPsocket.close()
            print('Connection lost')
            break
    #--------------------------------------------------------#

    # 정수를 전송하고 제곱 값을 받기
    #--------------------------------------------------------#
    while certified:
        print("정수 값 입력 : ", end='')
        value = input()
        try:
            # int로 바뀌는지 try
            int(value)
            value = Encryptor.encrypt(value.encode())
            TCPsocket.sendall(value)
            print("전송받은 제곱 값 : ", int.from_bytes(Encryptor.decrypt(TCPsocket.recv(1024)), 'big'))
        except:
            print('올바른 정수 값을 입력하세요.')
    #--------------------------------------------------------#

        
# 클라이언트 구동을 위한 정보 저장
#ip = '192.168.22.3'
ip = '127.0.0.1'
port = 52522

# 클라이언트 구동
runClient(ip, port)