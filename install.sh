#!/bin/bash

echo "Installing dependencies"
apt -qq update
apt -qq install wireguard wireguard-tools -y

address=
server=

echo "Creating wireguard config"
met_pubkey=
priv_key=$(wg genkey | tee /etc/wireguard/privatekey)
pub_key=$(echo $priv_key | wg pubkey | tee /etc/wireguard/publickey)
ps_key=$(wg genpsk | tee /tmp/preshared)

cat << EOF > /etc/wireguard/wg0.conf

[Interface]
MTU = 1412
Address = ${address}/32
PrivateKey = ${priv_key}

[Peer]
PublicKey = ${met_pubkey}
PresharedKey = ${ps_key}
Endpoint = ${server}:51820
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 10

EOF

echo "Starting wireguard service"
systemctl start wg-quick@wg0.service
systemctl enable wg-quick@wg0.service

echo "Building python GUI"
python3 -m venv venv
venv/bin/pip install -e . -qq

echo "@lxterminal -e `pwd`/venv/bin/meticulous-gateway-gui" >> /etc/xdg/lxsession/LXDE-pi/autostart

echo "Install completed"

echo "Private Key:"
echo $priv_key

echo "Public Key:"
echo $pub_key

echo "copy the following into your servers wireguard config"
echo =========================================================
echo "# Meticulous Gateway ${address}"
echo "[Peer]"
echo "PublicKey = ${pub_key}"
echo "PresharedKey = ${ps_key}"
echo "AllowedIPs = ${address}/32"
echo =========================================================

