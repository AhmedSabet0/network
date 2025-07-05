from netmiko import ConnectHandler

#  R1
r1 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.101.200',
    'username': 'admin',
    'password': 'admin123',
    'fast_cli': False,
}

#  OSPF
remove_ospf_cmds = [
    'conf t',
    'no router ospf 1',
    'end',
    'wr'
]

print("[*] Connecting to R1...")
net_connect = ConnectHandler(**r1)
print("[+] Connected to R1")

print("[*] Removing OSPF from R1...")
for cmd in remove_ospf_cmds:
    net_connect.send_command_timing(cmd)

# === SSH R2 ===
print("[*] SSH  R2  R1...")
output = net_connect.send_command_timing("ssh -l admin 192.168.10.2")

if "yes/no" in output:
    output += net_connect.send_command_timing("yes")
if "Password:" in output:
    output += net_connect.send_command_timing("admin123")


output += net_connect.send_command_timing("\n")


print("[*] Removing OSPF from R2...")
for cmd in remove_ospf_cmds:
    output += net_connect.send_command_timing(cmd)


if "Overwrite the previous NVRAM configuration?[confirm]" in output:
    output += net_connect.send_command_timing("\n")


output += net_connect.send_command_timing("exit")


print("\n====[OUTPUT]====\n")
print(output)


net_connect.disconnect()
