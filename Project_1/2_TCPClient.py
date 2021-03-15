from AES_CBC import aes_CBC

# 통신을 위해 client 를 구동시키기 위한 함수
import socket
def runClient(ip, port, key, iv):
    # TCP 통신을 하기 위한 객체를 생성
    TCPsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 서버와 통신이 가능하게 될 때 까지 대기
    print('Waiting for Server...')
    if not TCPsocket.connect((ip, port)):
        print('Connected to File Server!')

    # 암호화 / 복호화를 위한 encryptor class 객체 생성
    Encryptor = aes_CBC(key, iv)

    # 종료를 위한 알림
    print("종료를 위해서, Enter ( wq! ) / 서버를 닫기 위해서, Enter ( close )")

    # 계속 파일 이름을 전송하고, 다운로드 받기 위함
    while True:
        # 파일 이름을 받는다.
        fileName = input("파일의 이름을 입력해 주세요 : ")
        # 서버에 파일 이름을 전송
        TCPsocket.sendall(Encryptor.encrypt(fileName.encode()))
        # Client 종료 명령어
        if fileName == "wq!":
            break
        # 서버에서 파일을 못 찾는다면 N을, 찾는다면 ready를 전송할 것이다.
        serverCall = TCPsocket.recv(512)
        message = Encryptor.decrypt(serverCall).decode()
        # 파일을 못 찾았을 때 처음부터 다시 해야함
        if message == 'N':
            print("그런 이름을 가진 파일은 없습니다!")
            continue

        # 파일을 찾았다면?
        elif message == "ready":
            # 파일 다운로드 여부를 물어봄
            message = input("파일을 다운로드 받으시겠습니까? (Y / N) : ")
            # 찬성 했을 시 데이터 전송
            if message == 'Y':
                TCPsocket.sendall(Encryptor.encrypt(message.encode()))
                transffered_size = 0
                data = Encryptor.decrypt(TCPsocket.recv(1024))
                with open('./download/' + fileName, 'wb') as writeFile:
                    try:
                        while data:
                            writeFile.write(data)
                            transffered_size = transffered_size + len(data)
                            data = Encryptor.decrypt(TCPsocket.recv(1024))
                    except Exception as e:
                        print(e)
                print("파일 [%s](%dbytes) 수신 완료" %(fileName, transffered_size))
            else:
                TCPsocket.sendall(Encryptor.encrypt(message.encode()))
                print("데이터 전송 취소")

# 클라이언트 구동을 위한 정보 저장
ip = '127.0.0.1'
port = 52522
key = b'\x1c&\xcd\x90\xf3\x8eLe\xe9\x97b\x11N+\x99\xa9\xf3VR\xbc\x9ee\xa4o\x7f\x87A\x18rY\x98}'
iv = b"\xb1\xd8\xcf\x12e'\xb2{;\x00\x0c\xc9Cw\xc0\x1e"

# 클라이언트 구동
runClient(ip, port, key, iv)