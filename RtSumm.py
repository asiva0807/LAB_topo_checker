from jnpr.junos import Device
from pprint import pprint
from lxml import etree

DevLoginDet = []

def RT_Summ(username, pwd, host ):
    return_dict = {}
    dev = Device(host=host, user=username, password=pwd)
    dev.open()
    rt_information = dev.rpc.get_route_summary_information()
    dev.close()
    rt_summary = rt_information.findall('.//route-table')
    for rtRecords in rt_summary:
        table_name = rtRecords.find('.//table-name').text
        destination_count = rtRecords.find('.//destination-count').text
        total_route_count = rtRecords.find('.//total-route-count').text
        active_route_count = rtRecords.find('.//active-route-count').text
        allProtoElementLst = rtRecords.findall('.//protocols')
        all_protocols =[]
        for elementData in allProtoElementLst:
            all_protocols.append(etree.tostring(elementData, encoding='unicode'))
        protoRec = ""
        for protoData in all_protocols:
            protoRec += ''.join(("Protocol Name:  ",(protoData.split("<protocol-name>")[1]).split("</protocol-name>")[0],"\n","Rt Count:  ",(protoData.split("<active-route-count>")[1]).split("</active-route-count>")[0],"\n"))
            AprotoRec = (protoData.split("<protocol-name>")[1]).split("</protocol-name>")[0]
            AprotoRec += "--> Rt Count:  "
            AprotoRec += (protoData.split("<active-route-count>")[1]).split("</active-route-count>")[0] 
            AprotoRec += "\n ================== \n"
        return_dict[table_name] = { 
            'Destn Count' : destination_count,
            'Total Rt Count' : total_route_count,
            'Active Rt Count' : active_route_count,
            'Protocol specific Rt cnt' : protoRec 
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
        pprint(RT_Summ(Dev[1], Dev[2], Dev[0]))
