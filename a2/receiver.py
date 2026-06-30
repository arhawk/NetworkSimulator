__author__      = "Zehao Liu", "Zhenggan Luo"
__copyright__   = "@2022 CP372 WLU"
__mortalright__  = "@2022 Zehao Liu reserved"

try:
    from .common import *
except ImportError:  # pragma: no cover
    from common import *

class receiver: # all seqNum=0
    
    def isCorrupted(self, packet):
        ''' Checks if a received packet has been corrupted during transmission.
        Return true if computed checksum is different than packet checksum.'''
        tempsum=packet.seqNum+packet.ackNum+checksumCalc(packet.payload)
        # print("isCorrupted: ",tempsum != packet.checksum)
        return tempsum != packet.checksum

    def isDuplicate(self, packet):
        '''checks if packet sequence number is the same as expected sequence number'''
        # print("isDuplicated")
        # print("receiver: self.ackNum, packet.seqNum", self.ackNum, packet.seqNum)
        return self.ackNum != packet.seqNum

    def getNextExpectedSeqNum(self):
        '''The expected sequence numbers are 0 or 1'''
        # print("next ack= ", self.ackNum)
        self.ackNum = abs(self.ackNum - 1)
        return 

    
    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing receiver: B: "+str(self.entity))


    def init(self):
        '''initialize expected sequence number'''
        self.seqNum = 0
        self.ackNum = 0
        self.checksum = 0
        self.packet =None
        return

    def input(self, packet):
        '''This method will be called whenever a packet sent 
        from the sender arrives at the receiver. If the received
        packet is corrupted or duplicate, it sends a packet where
        the ack number is the sequence number of the  last correctly
        received packet. Since there is only 0 and 1 sequence numbers,
        you can use the sequence number that is not expected.
        
        If packet is OK (not a duplicate or corrupted), deliver it to the
        application layer and send an acknowledgement to the sender
        '''
        # print("inside input")
        # print("isCorrupted: ",self.isCorrupted(packet))
        # print("isDuplicate: ",self.isDuplicate(packet))
        if self.isCorrupted(packet):
            # print("self.ackNum in corrupted= ",self.ackNum)
            p=Packet(self.seqNum, self.ackNum, self.checksum) #send present ackNum so that sender notice corrupt
            self.networkSimulator.udtSend(self.entity, p)
        elif self.isDuplicate(packet):
            self.networkSimulator.udtSend(self.entity, self.packet)
        else:
            self.checksum = self.seqNum+self.ackNum
            self.packet= Packet(self.seqNum, self.ackNum, self.checksum) #this packet may resend due to duplication
            # self.getNextExpectedSeqNum()
            # print("packet.seqNum",packet.seqNum)
            self.networkSimulator.deliverData(self.entity,self.packet)
            # print("B sending: ",self.seqNum, self.ackNum, self.checksum)
            self.networkSimulator.udtSend(self.entity, self.packet)
            # print("we get here first")
            # print(self.ackNum)
            self.getNextExpectedSeqNum()
            # print(self.ackNum)
        return
