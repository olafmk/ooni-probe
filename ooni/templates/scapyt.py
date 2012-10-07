# -*- encoding: utf-8 -*-
#
# :authors: Arturo Filastò
# :licence: see LICENSE

import random
from zope.interface import implements
from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.internet import protocol, defer

from scapy.all import *

from ooni.nettest import TestCase
from ooni.utils import log

from ooni.lib.txscapy import txsr, txsend

class ScapyTest(TestCase):
    """
    A utility class for writing scapy driven OONI tests.

    * pcapfile: specify where to store the logged pcapfile

    * timeout: timeout in ms of when we should stop waiting to receive packets

    * receive: if we should also receive packets and not just send
    """
    name = "Scapy Test"
    version = 0.1

    receive = True
    timeout = 1
    pcapfile = None
    input = IP()/TCP()
    reactor = None
    def setUp(self):
        if not self.reactor:
            from twisted.internet import reactor
            self.reactor = reactor
        self.request = {}
        self.response = {}

    def tearDown(self):
        self.reactor.stop()

    def sendReceivePackets(self, packets):
        d = txsr(packets, pcapfile=self.pcapfile,
                     timeout=10, reactor=self.reactor)

        return d

    def sendPackets(self, packets):
        return txsend(self.buildPackets(), reactor=self.reactor)

    def buildPackets(self):
        """
        Override this method to build scapy packets.
        """
        return self.input

