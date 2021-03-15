# 통신을 위해 server 를 구동시키기 위한 함수
import socket

from os.path import exists

def runServer(ip, port, key, iv):
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
    
    # ID, Password 확인하기
    #--------------------------------------------------------#
    certified = False
    while 1:
        certification = connection.recv(1024)

        with open('./pw', 'rb') as pwFile:
            line = "True"
            while line:
                line = pwFile.readline()
                if certification == line:
                    print('Authentication Complete : ' + line.decode('utf-8').split(" ")[0])
                    certified = True

        if certified:
            connection.send("True".encode('utf-8'))
            break
        else:
            connection.send("False".encode('utf-8'))
    #--------------------------------------------------------#

    # client 가 정수를 계속 입력할 수 있게 한다.
    #--------------------------------------------------------#
    while certified:
        # 받고 싶은 파일 이름을 수신 및 복호화
        clientCall = connection.recv(1024).decode('utf-8')
        
        # 서버를 닫으라고 명령을 내릴 때 서버 OFF
        if clientCall == "close":
            connection.close()
            return

        squaredValue = int(clientCall) * int(clientCall)
        print("Client가 전송한 정수 : ", clientCall, " 제곱 값 : ", squaredValue)
        connection.send(str(squaredValue).encode('utf-8'))
    #--------------------------------------------------------#


# 서버 구동을 위한 정보 저장
ip = '127.0.0.1'
port = 52522
key = b'\x1c&\xcd\x90\xf3\x8eLe\xe9\x97b\x11N+\x99\xa9\xf3VR\xbc\x9ee\xa4o\x7f\x87A\x18rY\x98}'
iv = b"\xb1\xd8\xcf\x12e'\xb2{;\x00\x0c\xc9Cw\xc0\x1e"

# 서버 구동
runServer(ip, port, key, iv)