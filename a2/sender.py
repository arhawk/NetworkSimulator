__author__      = "Zehao Liu", "Zhenggan Luo"
__copyright__   = "@2022 CP372 WLU"
__mortalright__  = "@2022 Zehao Liu reserved"

try:
    from .common import *
except ImportError:  # pragma: no cover
    from common import *

class sender: # all ackNum=0
    RTT = 20

    def isCorrupted(self, packet):
        '''Checks if a received packet (acknowledgement) has been corrupted
        during transmission.
        Return true if computed checksum is different than packet checksum.
        '''
        # print("sender: self.checksum, packet.checksum =", self.checksum, packet.checksum )
        tempsum=packet.seqNum+packet.ackNum+checksumCalc(packet.payload)
        # print("isCorrupted: ",tempsum != packet.checksum)
        return tempsum != packet.checksum

    def isDuplicate(self, packet):
        '''checks if an acknowledgement packet is duplicate or not
        similar to the corresponding function in receiver side
        '''
        # print("isDuplicate")
        # print("self.seqNum, packet.ackNum= ",self.seqNum, packet.ackNum)
        return self.seqNum != packet.ackNum

    def getNextSeqNum(self):
        '''generate the next sequence number to be used.
        '''
        self.seqNum = abs(self.seqNum - 1)
        return

    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing sender: A: " + str(self.entity))

    def init(self):
        '''initialize the sequence number and the packet in transit.
        Initially there is no packet is transit and it should be set to None
        '''
        self.seqNum = 0
        self.ackNum = 0
        self.checksum = 0
        self.msg = ''
        self.packet=None
        return

    def timerInterrupt(self): #for timer timeout behave
        '''This function implements what the sender does in case of timer
        interrupt event.
        This function sends the packet again, restarts the time, and sets
        the timeout to be twice the RTT.
        You never call this function. It is called by the simulator.
        '''
        self.networkSimulator.udtSend(self.entity, self.packet)
        self.networkSimulator.startTimer(self.entity, 2*float(self.RTT))
        return

    def output(self, message): #for loss resend infor
        '''prepare a packet and send the packet through the network layer
        by calling calling utdSend.
        It also start the timer.
        It must ignore the message if there is one packet in transit
        '''
        self.msg = message.data
        self.checksum = self.seqNum+self.ackNum+checksumCalc(self.msg)
        self.packet = Packet(self.seqNum, self.ackNum, self.checksum, self.msg)
        self.networkSimulator.udtSend(self.entity, self.packet)
        self.networkSimulator.startTimer(self.entity, float(self.RTT))
        return

    def input(self, packet): 
        '''If the acknowlegement packet isn't corrupted or duplicate, 
        transmission is complete. Therefore, indicate there is no packet
        in transition.
        The timer should be stopped, and sequence number  should be updated.

        In the case of duplicate or corrupt acknowlegement packet, it does 
        not do anything and the packet will be sent again since the
        timer will be expired and timerInterrupt will be called by the simulator.
        '''
        # print("in sender input function")
        # print("isCorrupted: ",self.isCorrupted(packet))
        # print("isDuplicate: ",self.isDuplicate(packet))
        if not (self.isCorrupted(packet) or self.isDuplicate(packet)):
            # print("neither corrupt nor duplicate")
            self.networkSimulator.stopTimer(self.entity)
            self.getNextSeqNum()
        return
