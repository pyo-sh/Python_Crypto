import socket
# DES3, CBC 암호화 방식을 사용하기 위한 불러오기
from DES3_CBC import des3_CBC
# Diffie-Hellman 방식을 사용하기 위한 불러오기
from Diffie_Hellman import diffieHellman

def runServer(ip, port, iv):
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
    
    # Diffie-Hellman 으로 통신하기 위함
    p = 9876437;    g = 19576
    keySetter = diffieHellman(p, g)
    a = 1234

    # Client의 Key 수신
    key = keySetter.getKey(int.from_bytes(connection.recv(1024), 'big'), a)
    print("A를 수신받았습니다. B를 전송중...")

    # Server의 Key 생성 및 전달
    serverValue = keySetter.setValue(a)
    connection.sendall(serverValue.to_bytes(16, 'big'))
    print("B를 전송하였습니다.")

    # 암호화 / 복호화를 위한 encryptor class 객체 생성
    Encryptor = des3_CBC(key, iv)

    # ID, Password 확인하기
    #--------------------------------------------------------#
    certified = False
    while 1:
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
            connection.send(Encryptor.encrypt("False".encode()))
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
ip = '192.168.22.3'
port = 52522
iv = b'\x91#{\x19\xf2r\xa5\x0c'

# 서버 구동
runServer(ip, port, iv)