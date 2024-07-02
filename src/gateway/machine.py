import logging

from serial.tools import list_ports


def is_serial_connected():
    try:
        serial_connections = sorted(list_ports.grep(r"(USB|ACM)", include_links=True))
        if len(serial_connections) == 0:
            return False, "Not connected to any machine"
        conn_string = "\n".join(
            [f"{x[0]}" for x in serial_connections]
        )
        return True, f"Connected to {len(serial_connections)} machine(s): \n{conn_string}"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"
