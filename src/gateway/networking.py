import nmcli
import requests
import logging

nmcli.disable_use_sudo()
nmcli.set_lang("C.UTF-8")

logging.getLogger("urllib3").setLevel(logging.INFO)


def is_wifi_connected():
    try:
        # Get the status of all Wi-Fi connections
        wifi_connections = nmcli.device.wifi()
        # Find the Wi-Fi connection that is active
        for connection in wifi_connections:
            if connection.in_use:
                ssid = connection.ssid
                return True, f"Connected to Wi-Fi network: {ssid}"
        return False, "Not connected to any Wi-Fi network"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"


def has_internet_connection(url="http://www.google.com/", timeout=5):
    try:
        # Make an HTTP GET request to the specified URL
        response = requests.get(url, timeout=timeout)
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            return True, "Internet connection is available."
        else:
            return False, f"Received unexpected status code {response.status_code}."
    except requests.RequestException as e:
        return False, f"No internet connection. Error: {str(e)}"


def is_wireguard_connected():
    try:
        # Get the status of all connections
        connections = nmcli.connection()
        wireguard_connections = list(
            filter(lambda a: a.conn_type == "wireguard", connections)
        )

    except Exception as e:
        return False, f"An error occurred: {str(e)}"

    if len(wireguard_connections) > 0:
        conn_string="\n".join(list(map(lambda wg: wg.name, wireguard_connections)))
        return (
            True,
            f"Connected to wireguard:\n{conn_string}"
        )
    else:
        return False, "Not connected to wireguard"


print(is_wireguard_connected())
