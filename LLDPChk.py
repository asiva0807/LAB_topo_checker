from jnpr.junos.op.lldp import LLDPNeighborTable 
from jnpr.junos.utils.config import Config
from jnpr.junos import Device
from pprint import pprint
from lxml import etree
import sys
DevLoginDet = []

def lldp_out(username, pwd, host):
    dev = Device(host=host, user=username, password=pwd)
    dev.open()
    cu = Config(dev)
    cu.load('set protocols lldp interface all', format='set')
    cu.pdiff()
    cu.commit()
    lldp_table = LLDPNeighborTable(dev)
    lldp_table.get()
    dev.close()
    return lldp_table.items()

if __name__ == "__main__":
    # to run the function against a single host
    NodeCnt = int(input("Enter the number nodes in the topology: \t"))
    for cnt in range(NodeCnt):
        DevIP = input("Enter the node IP address:\t")
        DevUser = input("Enter the user name: \t")
        DevPwd = input("Enter the password:\t")
        DevLoginDet.append([DevIP,DevUser,DevPwd])
    for Dev in DevLoginDet:
        pprint(lldp_out(Dev[1], Dev[2], Dev[0]))