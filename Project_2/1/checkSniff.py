from scapy.all import *

#scapy를 사용하기 위해 import 해준다. 

def showpacket(packet):
#패킷을 인자로 받아서, 패킷의 정보를 출력해주는 함수이다. 
    print(packet.show())
#packet.show()는 scapy에서 제공하는 함수로 캡처한 패킷에 대한 정보를 표준출력해준다.

def main(filter):
    sniff(filter = filter, prn = showpacket, count =1)
#sniff()의 인자로는 count , store, prn, filter, iface가 존재한다. 
#여기서 count는 패킷을 캡처하는 횟수를 지정해주는데 0 이면 사용자가 중지할 때 까지 캡처한다. 
#store는 캡처한 패킷의 저장 여부를 결정하고, 네트워크 모니터랑만 원할 때는 0으로 지정한다. 
#prn은 캡처한 패킷을 처리하기 위한 함수를 지정한다. 

#패킷을 받아서, 필터로 거른 다음의 결과를 출력해준다. 

if __name__ == '__main__':
    filter = 'ip'
    main(filter)
