# IPsecVPN_AWS
[Work in progress - the features will be fine tune in the coming days] 

This code runs in three parts:

++ StrongSwanNQuaggaInstall.sh (This shell script downloads Strongswan and Quagga and readies the config files for VPN creation)

++ vpncode.py (This code will take the values from configuration file that you download from AWS VPN Console)

++ Stage3.sh (This shell script will bring up the tunnel and the BGP neighborship
