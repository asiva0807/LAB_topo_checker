from jnpr.junos import Device
from pprint import pprint
from lxml import etree

DevLoginDet = []

def ISIS_Nbr_Ext(username, pwd, host ):
    return_dict = {}
    dev = Device(host=host, user=username, password=pwd)
    dev.open()
    isis_information = dev.rpc.get_isis_adjacency_information(extensive=True)
    dev.close()
    isis_neighbors = isis_information.findall('.//isis-adjacency')
    for neighbor in isis_neighbors:
        system_name = neighbor.find('.//system-name').text
        address = neighbor.find('.//ip-address').text
        interface = neighbor.find('.//interface-name').text
        level = neighbor.find('.//level').text
        uptime = neighbor.find('.//last-transition-time').text
        return_dict[interface] = { 
            'system-name' : system_name,
            'neighbor-address' : address,
            'interface-name' : interface,
            'adjacency-level' : level,
            'neighbor-adjacency-time' : uptime,
        }
    return return_dict

if __name__ == "__main__":
    # to run the function against a single host
    import sys

    NodeCnt = int(input("Enter the number nodes in the topology: \t"))
    for cnt in range(NodeCnt):
        DevIP = input("Enter the node IP address:\t")
        DevUser = input("Enter the user name: \t")
        DevPwd = input("Enter the password:\t")
        DevLoginDet.append([DevIP,DevUser,DevPwd])
    for Dev in DevLoginDet:
        pprint(ISIS_Nbr_Ext(Dev[1], Dev[2], Dev[0]))