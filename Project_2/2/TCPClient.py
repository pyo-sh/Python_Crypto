import socket
# DES3, CBC 암호화 방식을 사용하기 위한 불러오기
from DES3_CBC import des3_CBC

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
            value = value.encode()
            TCPsocket.sendall(value)
            print("전송받은 제곱 값 : " + TCPsocket.recv(1024).decode())
        except:
            print('올바른 정수 값을 입력하세요.')
    #--------------------------------------------------------#

        
# 클라이언트 구동을 위한 정보 저장
ip = '192.168.22.3'
port = 52522
key = b'-\xed\xfe\xb7\x83\x80\x8e\xfdR*Lc\x1a\xa4\n\x03'
iv = b'\x91#{\x19\xf2r\xa5\x0c'

# 클라이언트 구동
runClient(ip, port, key, iv)