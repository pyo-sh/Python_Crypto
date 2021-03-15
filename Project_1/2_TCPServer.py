from AES_CBC import aes_CBC

# 통신을 위해 server 를 구동시키기 위한 함수
import socket
from os.path import exists
def runServer(ip, port, key, iv):
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
    # 암호화 / 복호화를 위한 encryptor class 객체 생성
    Encryptor = aes_CBC(key, iv)
    # client 가 파일을 계속 요청할 수 있도록 반복
    while 1:
        # 받고 싶은 파일 이름을 수신 및 복호화
        clientCall = connection.recv(512)
        fileName = Encryptor.decrypt(clientCall).decode()
        
        # 서버를 닫으라고 명령을 내릴 때 서버 OFF
        if fileName == "close":
            connection.close()
            return
        # 존재하지 않는 파일일 경우 
        elif not exists(fileName):
            message = Encryptor.encrypt('N'.encode())
            connection.sendall(message)
            print("파일 [%s] 존재하지 않음" % fileName)
            continue

        print("Client 에서 요청하는 파일 : ", fileName)

        data_size = 0
        transffered_size = 0
        # 파일이 있으면 데이터 변수를 통해 받기
        with open(fileName, 'rb') as readFile:
            # Client 에게 준비되었다고 연락
            message = Encryptor.encrypt("ready".encode())
            connection.sendall(message)
            # Client 에게서 Y 메세지를 받으면 파일을 전송
            clientCall = connection.recv(512)
            message = Encryptor.decrypt(clientCall).decode()
            if message == 'Y':
                try:
                    # 파일을 1Kb 단위로 받습니다.
                    data = readFile.read(1024)
                    data_size += len(data)
                    # 파일을 전부 전송할 때 까지 반복
                    while data:
                        # 데이터를 암호화 해서 전송하기 위함입니다.
                        data = Encryptor.encrypt(data)
                        # 데이터 전송량을 기록하고
                        transffered_size += connection.send(data)
                        # 다음 파일 데이터를 읽습니다.
                        data = readFile.read(1024)
                        data_size += len(data)
                    # 파일 전송이 종료됐음을 전송해야 합니다. (아무것도 없는 상태)
                    connection.send(Encryptor.encrypt(''.encode()))
                    # 전송 된 파일 출력
                    print("파일 [%s](%dbytes) 전송 완료 (전송 데이터 : %d bytes)" %(fileName, data_size, transffered_size))
                 # 에러가 발생한다면 이에 대한 내용을 출력
                except Exception as e:
                    print(e)
            else:
                print("데이터 전송 취소")

# 서버 구동을 위한 정보 저장
ip = '127.0.0.1'
port = 52522
key = b'\x1c&\xcd\x90\xf3\x8eLe\xe9\x97b\x11N+\x99\xa9\xf3VR\xbc\x9ee\xa4o\x7f\x87A\x18rY\x98}'
iv = b"\xb1\xd8\xcf\x12e'\xb2{;\x00\x0c\xc9Cw\xc0\x1e"

# 서버 구동
runServer(ip, port, key, iv)