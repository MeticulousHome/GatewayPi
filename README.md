# GatewayPi
Small GUI app for the UI on the Meticulous Gateway Raspberry PIs

## Install on Raspberry Pi
run 
```
sudo ./install.sh
```

it will automatically setup a venv for the project and create the script link `meticulous-gateway-gui`

## Install for development
```
python3 -m venv venv
source venv/bin/activate
pip install -e .
```
now it can be started with 
```
meticulous-gateway-gui
```

