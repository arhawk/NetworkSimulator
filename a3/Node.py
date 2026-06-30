__author__      = "Zehao Liu"
__copyright__   = "@2022 CP372 WLU"
__mortalright__  = "@2022 Zehao Liu reserved"

try:
    from .common import *
except ImportError:  # pragma: no cover
    from common import *

class Node:
    def __init__(self, ID, networksimulator, costs):
        self.myID = ID
        self.ns = networksimulator
        num = self.ns.NUM_NODES        

        self.routes = [999 for _ in range(num)]

        # you implement the rest of constructor
        
        self.neighbours=[]
        self.distanceTable = []
        
        #inital Distance Tables
        for i in range(num):
            lst=[]
            for j in range(num):
                if i==j:
                    lst.append(0)
                else:
                    lst.append(999)
            self.distanceTable.append(lst)
            # updata self.router
            if costs[i]!=999:
                self.routes[i]=i
        self.distanceTable[self.myID]=costs

        
        # assgin TOLAYER2 message and add neighbour for each router
        sourceId=self.myID
        costsInSouceId=self.distanceTable[sourceId]
        num = self.ns.NUM_NODES
        for i in range(num):
            destId=i
            if sourceId!=destId and costsInSouceId[i]!=999:
                self.neighbours.append(destId)
                rtP=RTPacket(sourceId,destId,costsInSouceId)
                self.ns.tolayer2(rtP)
        

    def recvUpdate(self, pkt):
        
        self.distanceTable[pkt.sourceid] = pkt.mincosts
        
        # you implement the rest of it  
        # self.printdt()
        num=self.ns.NUM_NODES 
        for dest in range(num):
            # print('sender, receiver:',pkt.sourceid,self.myID)
            a2c=self.distanceTable[self.myID][dest]
            a2b=self.distanceTable[self.myID][pkt.sourceid]
            b2c=self.distanceTable[pkt.sourceid][dest]
            # print('There to is here',a2c,a2b,b2c)
            if dest!=pkt.sourceid and dest!=pkt.destid:
                if a2c> a2b+b2c:
                    # if self.myID==0:
                    #     print(self.routes)
                    #     print("===================router change it table================")
                    #     print("=============nextHop changed=========original path, dest path",self.routes[dest],pkt.sourceid)
                    self.routes[dest]=self.routes[pkt.sourceid]

                    self.distanceTable[self.myID][dest]=a2b+b2c
                    self.__TOLAYER2message__()
        return 

    def __TOLAYER2message__(self):
        sourceId=self.myID
        costsInSouceId=self.distanceTable[sourceId]
        for destId in self.neighbours:
            rtP=RTPacket(sourceId,destId,costsInSouceId)
            self.ns.tolayer2(rtP)

    def printdt(self):
        print("   D"+str(self.myID)+" |  ", end="")
        for i in range(self.ns.NUM_NODES):
            print("{:3d}   ".format(i), end="")
        print()
        print("  ----|-", end="")
        for i in range(self.ns.NUM_NODES):            
            print("------", end="")
        print()    
        for i in range(self.ns.NUM_NODES):
            print("     {}|  ".format(i), end="" )
            
            for j in range(self.ns.NUM_NODES):
                print("{:3d}   ".format(self.distanceTable[i][j]), end="" )
            print()            
        print()
        
