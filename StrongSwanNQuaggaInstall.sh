#./bin/bash

sudo apt-get install -y strongswan quagga
sleep 30

echo net.ipv4.ip_forward=1 >> /etc/sysctl.conf
sleep 3

sudo touch /etc/quagga/zebra.conf
sleep 1

sudo touch /etc/quagga/bgpd.conf
sleep 1

sudo touch /etc/quagga/vtysh.conf
sleep 1

sudo chown quagga.quaggavty /etc/quagga/*.conf
sleep 1

sudo chmod 640 /etc/quagga/*.conf
sleep 1

> /etc/quagga/daemons
sudo echo zebra=yes >> /etc/quagga/daemons
sudo echo bgpd=yes >> /etc/quagga/daemons
sudo echo ospfd=no >> /etc/quagga/daemons
sudo echo ospf6d=no >> /etc/quagga/daemons
sudo echo ripd=no >> /etc/quagga/daemons
sudo echo ripngd=no >> /etc/quagga/daemons
sudo echo isisd=no >> /etc/quagga/daemons
sudo echo babeld=no >> /etc/quagga/daemons
sleep 3


echo install_routes = no >> /etc/strongswan.d/charon.conf
sleep 2

echo export VTYSH_PAGER=more >> /etc/bash.bashrc
sleep 2

echo VTYSH_PAGER=more >> /etc/environment
echo Installation Complete!
#log out and log back in
