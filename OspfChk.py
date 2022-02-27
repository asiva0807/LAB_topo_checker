from jnpr.junos import Device
from pprint import pprint
from lxml import etree

DevLoginDet = []

def jun_ospf_neighbor_extensive(username, pwd, host ):
    return_dict = {}
    dev = Device(host=host, user=username, password=pwd)
    dev.open()
    ospf_information = dev.rpc.get_ospf_neighbor_information(extensive=True)
    dev.close()
    ospf_neighbors = ospf_information.findall('.//ospf-neighbor')
    for neighbor in ospf_neighbors:
        #print(etree.tostring(neighbor, pretty_print=True)) 
        neighbor_id = neighbor.find('.//neighbor-id').text
        address = neighbor.find('.//neighbor-address').text
        interface = neighbor.find('.//interface-name').text
        uptime = neighbor.find('.//neighbor-adjacency-time').attrib['seconds']
        return_dict[interface] = { 
            'neighbor-id' : neighbor_id,
            'neighbor-address' : address,
            'interface-name' : interface,
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
        pprint(jun_ospf_neighbor_extensive(Dev[1], Dev[2], Dev[0]))
