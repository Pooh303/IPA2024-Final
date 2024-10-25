from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.183"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}

def gigabit_status():
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        interface_statuses = []
        result = ssh.send_command("show ip interface brief", use_textfsm=True)
        for interface in result:
            if "Gi" in interface['interface']:
                status = interface['status']
                interface_statuses.append(f"{interface['interface']} {status}")
                if status == "up":
                    up += 1
                elif status == "down":
                    down += 1
                elif status == "administratively down":
                    admin_down += 1

        status_string = ", ".join(interface_statuses)
        summary = f"-> {up} up, {down} down, {admin_down} administratively down"
        ans = f"{status_string} {summary}"
        pprint(ans)
        return ans