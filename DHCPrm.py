import paramiko
import time

def remove_dhcp(ip, username, password, interface):
    commands = [
        "conf t",
        "no ip dhcp excluded-address 192.168.100.1 192.168.100.10",
        "no ip dhcp pool DHCP_POOL",
        f"interface {interface}",
        "no ip address",
        "shutdown",
        "end",
        "wr"
    ]

    print(f"[+] Connecting to {ip}...")

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ip, username=username, password=password)

        shell = client.invoke_shell()
        time.sleep(1)

        for cmd in commands:
            shell.send(cmd + "\n")
            time.sleep(1)
            output = shell.recv(65535).decode()
            if "confirm" in output.lower():
                shell.send("\n")

        print("[+] DHCP configuration removed.")
        client.close()

    except Exception as e:
        print(f"[-] Failed to connect: {e}")

# Example usage:
remove_dhcp("192.168.100.1", "admin", "admin123", "FastEthernet2/0")