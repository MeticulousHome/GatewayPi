#!/bin/bash

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root" 1>&2
  exit 1
fi

# Read and validate input parameters
if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <IP_ADDRESS> <SERVER> <SERVER_PUBKEY>"
  exit 1
fi

echo "Installing dependencies"
apt -qq update
apt -qq install wireguard wireguard-tools fonts-noto-color-emoji -y

address=$1
server=$2

pi_user=meticulous

echo "Creating wireguard config"
met_pubkey=$3
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

mkdir -p /home/${pi_user}/.config/autostart

cat << EOF > /home/${pi_user}/.config/autostart/gateway.desktop
[Desktop Entry]
Type=Application
Name=GatewayGUI
Exec=bash -lhc "`pwd`/venv/bin/meticulous-gateway-gui &> `pwd`/../meticulous-gateway-gui.log"

EOF

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

