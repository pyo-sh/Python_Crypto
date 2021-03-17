# 통신을 위해 client 를 구동시키기 위한 함수
import socket

def runClient(ip, port, key, iv):
    # 연결하기
    #--------------------------------------------------------#
    # TCP 통신을 하기 위한 객체를 생성
    TCPsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 서버와 통신이 가능하게 될 때 까지 대기
    print('Waiting for Server...')
    if not TCPsocket.connect((ip, port)):
        print('Connected to File Server!')
    #--------------------------------------------------------#

    # 인증
    #--------------------------------------------------------#
    certified = False
    while not certified:
        print("[ID Password]를 입력해주세요")
        # 입력 받고 byte로 변경
        getAuthentication = input().encode('utf-8')
        TCPsocket.sendall(getAuthentication)
        if TCPsocket.recv(1024).decode('utf-8') == "True":
            certified = True
            print('Authentication Complete')
        else:
            print('Authentication Failed')
    #--------------------------------------------------------#

    # 정수를 전송하고 제곱 값을 받기
    #--------------------------------------------------------#
    while certified:
        print("정수 값 입력 : ", end='')
        value = input()
        try:
            # int로 바뀌는지 try
            int(value)
            value = value.encode('utf-8')
            TCPsocket.sendall(value)
            print("전송받은 제곱 값 : " + TCPsocket.recv(1024).decode('utf-8'))
        except:
            print('올바른 정수 값을 입력하세요.')
    #--------------------------------------------------------#

        
# 클라이언트 구동을 위한 정보 저장
ip = '127.0.0.1'
port = 52522
key = b'\x1c&\xcd\x90\xf3\x8eLe\xe9\x97b\x11N+\x99\xa9\xf3VR\xbc\x9ee\xa4o\x7f\x87A\x18rY\x98}'
iv = b"\xb1\xd8\xcf\x12e'\xb2{;\x00\x0c\xc9Cw\xc0\x1e"

# 클라이언트 구동
runClient(ip, port, key, iv)