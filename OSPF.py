import yaml
from netmiko import ConnectHandler

# impoty YAML file for Routers
with open("ospf_config.yaml", "r") as file:
    data = yaml.safe_load(file)

# loop in routers
for router in data["routers"]:
    print(f" Connecting to {router['name']} ({router['ip']})...")

    device = {
        "device_type": "cisco_ios",
        "ip": router["ip"],
        "username": router["username"],
        "password": router["password"],
    }

    try:
        connection = ConnectHandler(**device)
        print(f" Connected to {router['name']}")

        #  OSPF
        commands = [
            "router ospf 1",
            f"network {router['loopback']} 0.0.0.0 area 0"
        ]

        for net in router["ospf_networks"]:
            cmd = f"network {net['network']} {net['wildcard']} area {net['area']}"
            commands.append(cmd)

        output = connection.send_config_set(commands)
        print(f" OSPF Configured on {router['name']}:\n{output}")

        connection.disconnect()

    except Exception as e:
        print(f" Error on {router['name']}: {e}")