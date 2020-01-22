
import subprocess
import socket
import sys

# This step will install strongswan and quagga and make it ready to setup ipsec vpn

subprocess.call(['./StrongSwanNQuaggaInstall.sh'])


print('Enter the configuration for primary tunnel \nEnter the VGW IP')
VGW1 = str(input())

print('Enter the Pre-Shared Key')
PSK = str(input())

print('Enter Your Side IP from Tunnel Inside CIDR')
Tun1 = str(input())

print('Enter AWS side IP from Tunnel Inside CIDR ')
Tun2 = str(input())

print('Enter your BGP ASN')
ASN1 = input()

print('Enter AWS side BGP ASN')
ASN2 = input()

print('Enter your side of the lan')
LAN = str(input())

hostname = socket.gethostname()
IPaddr = socket.gethostbyname(hostname)

with open('/etc/ipsec.conf' ,'w') as myfile1:
    file.close()

line1 = "conn vpn-123456\n"
line2 = "type=tunnel\n"
line3 = "authby=psk\n"
line4 = "left=IPaddr\n"
line5 = "right=VGW1\n"
line6 = "keyexchange=ikev1\n"
line7 = "auto=start\n"
line8 = "ike=aes128-sha1-modp1024\n"
line9 = "esp=aes128-sha1-modp1024\n"
line10 = "leftsubnet=0.0.0.0/0\n"
line11 = "rightsubnet=0.0.0.0/0\n"
line12 = "ikelifetime=8h\n"
line13 = "keylife=1h\n"
line14 = "mobike=no\n"
line15 = "dpdaction=restart\n"
line16 = "dpddelay=10s\n"
line17 = "dpdtimeout=30s\n"
line18 = "mark=111\n"


with open('/etc/ipsec.conf' ,'a') as out:
    out.writelines \
        ([line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12, line13, line14, line15, line16, line17 ,line18])
    out.close()

with open('/etc/ipsec.secrets' ,'a') as myfile:
    myfile.write('%s %s:%s '% (IP, VGW1, PSK))

orig_stdout = sys.stdout
f = open('stage3.sh', 'w')
sys.stdout = f

while True:
    print(f'sudo ip link add vpn-123456 type vti key 111 remote {VGW} local {IPaddr}')
    print(f'sudo ip addr add {Tun1} remote {Tun2} dev vpn-123456')
    print('sudo ip link set vpn-123456 up mtu 1436')
    print('sudo iptables -t mangle -A FORWARD -o vpn-123456 -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu')
    print('sudo sysctl -w net.ipv4.conf.vpn-123456.rp_filter=2')
    print('sudo sysctl -w net.ipv4.conf.vpn-123456.disable_policy=1')
    print('net.ipv4.conf.eth0.disable_policy = 1')
    print('net.ipv4.conf.eth0.disable_xfrm = 1\nsleep 3')
    print('sudo service networking restart\nsleep 3\nsudo vtysh\nconf t')
    print(f'router bgp {ASN1}')
    print(f'network {LAN}')
    print(f'neighbor {Tun2} remote {ASN2}')
    print(f'neighbor {Tun2} soft-reconfiguration inbound')
    print('end')
    print('wr\nsleep 10')
    print('exit')
    print('sudo service quagga restart\nsudo vtysh')
    print('clear ip bgp *')

        sys.stdout = orig_stdout
        f.close()
        break

#subprocess.call(['./StrongSwannQuaggaInstall.sh'])
