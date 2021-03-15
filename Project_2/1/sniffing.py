from scapy.all import *

protocols = {1: 'ICMP', 6: 'TCP', 17:'UDP'}

def showpacket(packet):
    src_ip = packet[0][1].src
    dst_ip = packet[0][1].dst
    proto  =packet[0][1].proto

    if proto in protocols:
        print('protocol : %s: %s -> %s' %(protocols[proto], src_ip,dst_ip))
        if proto == 1:
            print('type:[%d], code:[%d]' %(packet[0][2].type, packet[0][2].code))

def main(filter):
    sniff(filter =filter, prn = showpacket, count = 0)
#count가 0이므로 모니터링 모드이다.

if __name__ == '__main__':
    main(filter)