

import socket
import sys

print('Enter the configuration for primary tunnel \nYour VPN Connection ID')
vpnid=str(input())
vpnvti, vpnvti2 = vpnid[:len(vpnid)//2], vpnid[len(vpnid)//2:]

print('Enter the Customer Gateway IP')
CGW = str(input())

print('Enter the Virtual Private Gateway IP')
VGW1 = str(input())

print('Enter the Pre-Shared Key')
PSK = str(input())

print('Enter Inside IP Addresse of Customer Gateway. Only enter the IP without any subnet mask')
Tun1 = str(input())

print('Enter Inside IP Addresses of Virtual Private Gateway . Only enter the IP without any subnet mask ')
Tun2 = str(input())

print('BGP Configuration Options:\nCustomer Gateway ASN')
ASN1 = input()

print('Virtual Private Gateway ASN')
ASN2 = input()

print('Enter your side of the LAN cidr range that will connect to VPC resources. e.g 192.168.1.0/24')
LAN = str(input())

hostname = socket.gethostname()
IPaddr = socket.gethostbyname(hostname)

with open('/etc/ipsec.conf','a') as myfile1:
    myfile1.close()

line1 = "config setup\n"
line2 = "conn vpn-123456\n"
line3 = "\ttype=tunnel\n"
line4 = "\tauthby=psk"
line5 = "\n\tleft="
line6 = "\n\tleftid="
line7 = "\n\tright="
line8 = "\n\tkeyexchange=ikev1\n"
line9 = "\tauto=start\n"
line10 = "\tike=aes128-sha1-modp1024\n"
line11 = "\tesp=aes128-sha1-modp1024\n"
line12 = "\tleftsubnet=0.0.0.0/0\n"
line13 = "\trightsubnet=0.0.0.0/0\n"
line14 = "\tikelifetime=8h\n"
line15 = "\tkeylife=1h\n"
line16 = "\tmobike=no\n"
line17 = "\tdpdaction=restart\n"
line18 = "\tdpddelay=10s\n"
line19 = "\tdpdtimeout=30s\n"
line20 = "\tmark=111\n"


with open('/etc/ipsec.conf' ,'a') as out:
    out.writelines ([line1, line2, line3, line4, line5+IPaddr, line6+CGW, line7+VGW1, line8, line9, line10, line11, line12, line13, line14, line15, line16, line17 ,line18, line19, line20])
    out.close()

with open('/etc/ipsec.secrets' ,'a') as myfile:
    myfile.write('%s %s : PSK "%s" '% (IPaddr, VGW1, PSK))

orig_stdout = sys.stdout
f = open('stage3.sh', 'w')
sys.stdout = f

while True:
    print('sudo ip link add %s type vti key 111 remote %s local %s' % (vpnvti, VGW1, IPaddr))
    print('sudo ip addr add %s/30 remote %s/30 dev %s' % (Tun1, Tun2, vpnvti))
    print('sudo ip link set %s up mtu 1436' % (vpnvti))
    print('sudo iptables -t mangle -A FORWARD -o %s -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu' % (vpnvti))
    print('sudo sysctl -w net.ipv4.conf.%s.rp_filter=2' % (vpnvti))
    print('sudo sysctl -w net.ipv4.conf.%s.disable_policy=1' % (vpnvti))
    print('sudo sysctl -w net.ipv4.conf.eth0.disable_policy=1')
    print('sudo sysctl -w net.ipv4.conf.eth0.disable_xfrm=1\nsleep 3')
    print('sudo service networking restart')

    sys.stdout = orig_stdout
    f.close()
    break

with open('/etc/quagga/bgpd.conf','a') as bgpd:
    bgpd.write('router bgp %s\n bgp router-id %s\n network %s\n neighbor %s remote-as %s\n neighbor %s soft-reconfiguration inbound\n!\nline vty\n!' % (ASN1, IPaddr, LAN, Tun2, ASN2, Tun2))
    bgpd.close()

with open('/etc/quagga/zebra.conf','a') as zebra:
    zebra.write('interface eth0\n no link-detect\n ipv6 nd suppress-ra\n!\n')
    zebra.close()

with open('/etc/quagga/zebra.conf', 'a') as zebra2:
    zebra2.write('interface ip_vti0\n no link-detect\n ipv6 nd suppress-ra\n!\n')
    zebra2.close()

with open('/etc/quagga/zebra.conf', 'a') as zebra3:
    zebra3.write('interface lo\n no link-detect\n!\n')
    zebra3.close()

with open('/etc/quagga/zebra.conf', 'a') as zebra4:
    zebra4.write('interface %s\n no link-detect\n ipv6 nd suppress-ra\n!\nline vty\n!\n' % (vpnvti))
    zebra4.close()

print('A file name stage3.sh is now created. You need to execute this file and the vpn and bgp should come up. You might have restart the networking, strongswan and quagga service if it does not come up')
