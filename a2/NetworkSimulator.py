from __future__ import annotations

import random
from copy import deepcopy
from dataclasses import dataclass

try:
    from .common import A, B, Event, EventList, EventType, Message, MAXDATASIZE
    from .receiver import receiver
    from .sender import sender
except ImportError:  # pragma: no cover
    from common import A, B, Event, EventList, EventType, Message, MAXDATASIZE
    from receiver import receiver
    from sender import sender


@dataclass
class A2Scenario:
    max_messages: int = 5
    loss_prob: float = 0.0
    corrupt_prob: float = 0.0
    avg_delay: float = 1.0
    seed: int = 10
    trace: int = 1


class NetworkSimulator:
    def __init__(self):
        self.eventList = EventList()
        self.sender = None
        self.receiver = None
        self.maxMessages = 0
        self.lossProb = 0.0
        self.corruptProb = 0.0
        self.avgMessageDelay = 0.0
        self.rand = None
        self.nMsgSim = 0
        self.time = 0.0
        self.trace = 1
        self.delivered_messages = []

    def initSimulator(self, maxMsgs, loss, corrupt, delay, seed, trace):
        self.maxMessages = maxMsgs
        self.lossProb = loss
        self.corruptProb = corrupt
        self.avgMessageDelay = delay
        self.rand = random.seed(seed)
        self.nMsgSim = 0
        self.time = 0.0
        self.trace = trace
        self.eventList = EventList()
        self.sender = sender(A, self)
        self.receiver = receiver(B, self)

    def runSimulator(self):
        self.sender.init()
        self.receiver.init()
        self.generateNextArrival()

        while True:
            next_event = self.eventList.removeNext()
            if next_event is None:
                break
            self.time = next_event.time

            if next_event.event_type == EventType.TIMERINTERRUPT:
                if next_event.entity == A:
                    self.sender.timerInterrupt()
            elif next_event.event_type == EventType.FROMNETWORK:
                if next_event.entity == A:
                    self.sender.input(next_event.packet)
                elif next_event.entity == B:
                    self.receiver.input(next_event.packet)
            elif next_event.event_type == EventType.FROMAPP:
                next_message = self._build_message()
                self.sender.output(Message(next_message))
                if self.nMsgSim < self.maxMessages:
                    self.generateNextArrival()

    def simulate(self):
        self.runSimulator()
        return self.delivered_messages

    def _build_message(self):
        token = chr(((self.nMsgSim - 1) % 26) + 97)
        return token * MAXDATASIZE

    def generateNextArrival(self):
        x = self.avgMessageDelay * random.random() * 2
        next_event = Event(self.time + x, EventType.FROMAPP, A)
        self.eventList.add(next_event)
        self.nMsgSim += 1

    def startTimer(self, entity, increment):
        timer_event = self.eventList.removeTimer(entity)
        if timer_event is not None:
            self.eventList.add(timer_event)
        else:
            self.eventList.add(Event(self.time + increment, EventType.TIMERINTERRUPT, entity))

    def stopTimer(self, entity):
        self.eventList.removeTimer(entity)

    def udtSend(self, entity, p):
        packet = deepcopy(p)
        destination = B if entity == A else A

        if random.random() < self.lossProb:
            if self.trace:
                print("udtSend: simulated packet loss")
            return

        if random.random() < self.corruptProb:
            if self.trace:
                print("udtSend: simulated packet corruption")
            packet.checksum += 1

        arrival = self.time + max(0.1, self.avgMessageDelay * (0.5 + random.random()))
        self.eventList.add(Event(arrival, EventType.FROMNETWORK, destination, packet))

    def deliverData(self, entity, p):
        self.delivered_messages.append((entity, p.payload))
        if self.trace:
            print(f"deliverData: entity={entity} payload={p.payload}")

