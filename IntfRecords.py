from jnpr.junos import Device
from pprint import pprint
from jnpr.junos.utils.config import Config
from lxml import etree
from prettytable import PrettyTable

def RetUpIntf(dev):
    intDict = {}
    intKey = ""
    intLst = []  
    filter1 = '<interface-information><physical-interface><name/><oper-status/></physical-interface></interface-information>'
    result = dev.rpc.get_interface_information(filter_xml=filter1)
    intRecs = etree.tostring(result, encoding='unicode')
    tmpLst = intRecs.split("\n")
    for detail in tmpLst:
        if "name" not in detail:
            if intKey == "":
                intKey = detail
                intData = ""
            else:
                intData = detail
                intDict[intKey]=intData
                intKey = ""
    for intf,intStatus in intDict.items():
        if intStatus == "up":
            if "xe" in intf or "ae" in intf or "ge" in intf or "et" in intf:
                intLst.append(intf)
    return(intLst)

def RetIntfProps(dev,intLst):
    phyintprop = []
    logintprop = []
    filter1 = '<interface-information><physical-interface><name/><oper-status/><interface-flapped/></physical-interface></interface-information>'
    filter2 = '<interface-information><physical-interface><logical-interface><name/><traffic-statistics><input-packets/><output-packets/></traffic-statistics></logical-interface></physical-interface></interface-information>'
    for ints in intLst:
        result1 = etree.tostring(dev.rpc.get_interface_information(interface_name=ints,filter_xml=filter1),encoding='unicode')
        result2 = etree.tostring(dev.rpc.get_interface_information(interface_name=ints,filter_xml=filter2),encoding='unicode')
        result1lst = result1.split("\n")
        result2lst = result2.split("\n")
        phyintprop.append([result1lst[1],result1lst[3],result1lst[5]])
        logintprop.append([result2lst[1],result2lst[3],result2lst[5]])
    return(phyintprop,logintprop)
