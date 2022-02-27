from jnpr.junos import Device
from pprint import pprint
from jnpr.junos.utils.config import Config
from lxml import etree
from prettytable import PrettyTable, ALL
from IntfRecords import RetUpIntf as RetUpIntf
from IntfRecords import RetIntfProps as RetIntfProps
from OspfChk import jun_ospf_neighbor_extensive as OspfNbrExtensive
from ARPChk import arp_out as ARPOut
from LLDPChk import lldp_out as LLDPOut
from ISISAdj import ISIS_Nbr_Ext as ISISNbrExt
from RtSumm import RT_Summ as RTSumm
from textwrap import fill

DevLoginDet = []


NodeCnt = int(input("Enter the number nodes in the topology: \t"))
for cnt in range(NodeCnt):
    DevIP = input("Enter the node IP address:\t")
    DevUser = input("Enter the user name: \t")
    DevPwd = input("Enter the password:\t")
    DevLoginDet.append([DevIP,DevUser,DevPwd])

for Dev in DevLoginDet:
    dev = Device(host=Dev[0],user=Dev[1],password=Dev[2],gather_facts=True,use_filter=True)
    dev.open()
    dev.timeout = 120
    print("##########################################")
    print("Record Details of :\t"+Dev[0])
    print("##########################################\n\n")
    intLstA = RetUpIntf(dev)
    phyintprop,logintprop = RetIntfProps(dev,intLstA)
    phyintTable = PrettyTable(["Name","Op Status","Uptime"])
    phyintTable.hrules=ALL
    logintTable = PrettyTable(["Int Name","In Pkt","Out Pkt"])
    logintTable.hrules=ALL
    print("===========================================")
    print("                INTF Records               ")
    print("===========================================")
    for item in phyintprop:
        phyintTable.add_row(item)
    for item in logintprop:
        logintTable.add_row(item)
    print(phyintTable)
    print(logintTable)
    dev.close()
    print("===========================================")
    print("           IGP-OSPF Nbr Data               ")
    print("===========================================")
    OspfDict = OspfNbrExtensive(Dev[1],Dev[2],Dev[0])
    OspfNbrTbl = PrettyTable(["Nbr Rtr ID","Nbr Addr","Intf Name","Uptime (sec)"])
    OspfNbrTbl.hrules=ALL
    for Intf,OspfRec in OspfDict.items():
        OspfRecLst=list(OspfRec.values())
        OspfNbrTbl.add_row(OspfRecLst)
    print(OspfNbrTbl)
    print("===========================================")
    print("           ARP Neighbor Data               ")
    print("===========================================")
    ARPlrnTbl = PrettyTable(["Lrnt MAC","Lrnt IP","Interface"])
    ARPlrnTbl.hrules=ALL
    ARPdata = ARPOut(Dev[1],Dev[2],Dev[0])
    for ARPRec in ARPdata:
        ARPlrnTbl.add_row([ARPRec[1][0][1],ARPRec[1][1][1],ARPRec[1][2][1]])
    print(ARPlrnTbl)
    print("===========================================")
    print("           LLDP NBR Data                   ")
    print("===========================================")
    LLDPlrnTbl = PrettyTable(['Local Intf','Local Parent','Remote Type','Remote Chassis Id','Remote Port Desc','Remote Port#','Remote Sysname'])
    LLDPlrnTbl.hrules=ALL
    LLDPData = LLDPOut(Dev[1],Dev[2],Dev[0])
    for LLDPRec in LLDPData:
        LLDPlrnTbl.add_row([LLDPRec[1][0][1],LLDPRec[1][1][1],LLDPRec[1][2][1],LLDPRec[1][3][1],LLDPRec[1][4][1],LLDPRec[1][5][1],LLDPRec[1][6][1]])
    print(LLDPlrnTbl)
    print("===========================================")
    print("                IGP-ISIS Nbr Da            ")
    print("===========================================")
    ISISNbrTbl = PrettyTable(['Adjacency Level','Interface Name','Neighbor Address','Neighbor Adjacency Time','Peer System Name'])
    ISISNbrTbl.hrules=ALL
    ISISDict = ISISNbrExt(Dev[1],Dev[2],Dev[0])
    for Intf,ISISRec in ISISDict.items():
        ISISRecLst=list(ISISRec.values())
        ISISNbrTbl.add_row(ISISRecLst)
    print(ISISNbrTbl)
    print("===========================================")
    print("                Routing Data               ")
    print("===========================================")
    RtTbl = PrettyTable(['Table ID','Active Rt Count','Destn Count','Total Rt Count','Protocol specific Rt cnt'])
    RtTbl._max_width = { "Field 5" : 25}
    RtTbl.hrules=ALL
    RtRecs = RTSumm(Dev[1],Dev[2],Dev[0])
    for TblNm, RtDet in RtRecs.items():
        RtLst = []
        RtLst.append(TblNm)
        for n in list(RtDet.values()):
            RtLst.append(n)
        RtTbl.add_row([RtLst[0],RtLst[1],RtLst[2],RtLst[3],fill(RtLst[4], width=150)])
    print(RtTbl)



