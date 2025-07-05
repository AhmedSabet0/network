import yaml
import paramiko
import time

# Import YAML
with open("dhcp_config.yaml", "r") as file:
    data = yaml.safe_load(file)

# DHCP router configure for ssh 
def configure_router(router):
    ip = router["ip"]
    username = router["username"]
    password = router["password"]
    dhcp = router["dhcp"]  #DHCP configrations 

    commands = [
        "conf t",
        f"ip dhcp excluded-address {dhcp['excluded'][0]} {dhcp['excluded'][1]}",
        "ip dhcp pool DHCP_POOL",
        f" network {dhcp['network']} {dhcp['netmask']}",
        f" default-router {dhcp['gateway_ip']}",
        f" dns-server {dhcp['dns']}",
        f" lease {dhcp['lease']['days']} {dhcp['lease']['hours']}",
        "exit",
        f"interface {dhcp['interface']}",
        f" ip address {dhcp['gateway_ip']} {dhcp['netmask']}",
        " no shutdown",
        "end",
        "wr"
    ]
      # tre to ssh 
    try:
        print(f"[+] Connecting to {router['name']} ({ip})...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ip, username=username, password=password)
        shell = client.invoke_shell()

        for cmd in commands:
            shell.send(cmd + "\n")
            time.sleep(1)  # delay fo router
            output = shell.recv(10000).decode()
            if "confirm" in output.lower():
                shell.send("\n")

        print(f"[+] DHCP done on {router['name']}")
        client.close()

    except Exception as e:
        print(f"[-] Error on {router['name']}: {e}")

# for loop in routers   
for router in data["routers"]:
    configure_router(router)
