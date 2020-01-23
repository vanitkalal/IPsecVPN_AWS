
import subprocess
import socket
import sys

# This step will install strongswan and quagga and make it ready to setup ipsec vpn

#subprocess.call(['./StrongSwanNQuaggaInstall.sh'])

#subprocess.call(shlex.split(EDITOR) + ["StrongSwanNQuaggaInstall.sh"])

print('Enter the configuration for primary tunnel \nEnter the CGW IP')
CGW = str(input())

print('Enter the VGW IP')
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

with open('/etc/ipsec.conf' ,'a') as myfile1:
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
    out.writelines \
        ([line1, line2, line3, line4, line5+IPaddr, line6+CGW, line7+VGW1, line8, line9, line10, line11, line12, line13, line14, line15, line16, line17 ,line18, line19, line20])
    out.close()

with open('/etc/ipsec.secrets' ,'a') as myfile:
    myfile.write('%s %s : PSK "%s" '% (IPaddr, VGW1, PSK))

orig_stdout = sys.stdout
f = open('stage3.sh', 'w')
sys.stdout = f

while True:
    print('sudo ip link add vpn-123456 type vti key 111 remote %s local %s' % (VGW1, IPaddr))
    print('sudo ip addr add %s remote %s dev vpn-123456' % (Tun1, Tun2))
    print('sudo ip link set vpn-123456 up mtu 1436')
    print('sudo iptables -t mangle -A FORWARD -o vpn-123456 -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu')
    print('sudo sysctl -w net.ipv4.conf.vpn-123456.rp_filter=2')
    print('sudo sysctl -w net.ipv4.conf.vpn-123456.disable_policy=1')
    print('sudo sysctl -w net.ipv4.conf.eth0.disable_policy=1')
    print('sudo sysctl -w net.ipv4.conf.eth0.disable_xfrm=1\nsleep 3')
    print('sudo service networking restart\nsleep 3\nsudo vtysh\nconf t')
    print('router bgp %s' % (ASN1))
    print('network %s' % (LAN))
    print('neighbor %s remote %s' % (Tun2, ASN2))
    print('neighbor %s soft-reconfiguration inbound' % (Tun2))
    print('end')
    print('wr\nsleep 10')
    print('exit')
    print('sudo service quagga restart\nsudo vtysh')
    print('clear ip bgp *')

    sys.stdout = orig_stdout
    f.close()
    break

#subprocess.call(['./StrongSwannQuaggaInstall.sh'])
