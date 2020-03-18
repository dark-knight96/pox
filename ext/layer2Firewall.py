#Simple layer 2 firewall

from pox.core import core
import sqlmanager as sql
from pox.lib.revent import *
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import EthAddr
import constants as cn

if core != None:
    log = core.getLogger()

class layer2Firewall(EventMixin):
    def __init__(self):
        self.rules = utilMethods.getOnlyRules(utilMethods.getFireWallRules())
        print("Firewall rules loaded")
        self.listenTo(core.openflow)
        print("Starting layer2Firewall")

    def updateRules(self):
        self.rules = utilMethods.getOnlyRules(utilMethods.getFireWallRules())
    def _handle_ConnectionUp(self, event):

        self.updateRules()
        for rule in self.rules:
            matchInstance = of.ofp_match()
            matchInstance.dl_src = EthAddr(rule[0])
            matchInstance.dl_dst = EthAddr(rule[1])

            #Setting port blocks using TCP or UDP
            if str(rule[4]) != str(None):
                matchInstance.dl_type = cn.protoCodes["IPV4"]
                matchInstance.nw_proto = cn.protoCodes[rule[4]]
                if str(rule[2]) != str(None):
                    matchInstance.tp_src = int(rule[2])
                elif str(rule[3]) != str(None):
                    matchInstance.tp_dst = int(rule[3])
            #Sending new flow mod message
            flowMod = of.ofp_flow_mod()
            flowMod.match = matchInstance
            event.connection.send(flowMod)

        from pox.listener import updateBootCore #deferring circular imports
        updateBootCore()

class utilMethods():
    @staticmethod
    def constructmatchStructure(rule, protocol = None, port=None):
        match = of.ofp_match()
        match.dl_src = EthAddr(rule[0])
        match.dl_dst = EthAddr(rule[1])
        if protocol != None  and port != None:
            # For blocking TCP and UDP traffic
            match.dl_type = 0x800   #setting Ether packet type as IPV4
            if protocol == "TCP" or protocol == "UDP":
                match.nw_proto = cn.protoCodes[protocol]
                if port[cn.SRC_PORT] != str(None):
                    match.tp_src = int(port[cn.SRC_PORT])
                if port[cn.DEST_PORT] != str(None):
                    match.tp_dst = int(port[cn.DEST_PORT])
        return match
    def __init__(self):
        """
        Empty constructor
        """
    @staticmethod
    def getFireWallRules():
        """
        :return: Fetches all firewall rules as a list of tuples
        """
        rules = sql.fetchAllRecords("layer2")
        return rules
    @staticmethod
    def getOnlyRules(rules):
        """
        :param rules: a list of tuples of formar [(switchid, source_mac, dest_mac)]
        :return: a list containing only the mac addresses [[source_mac, dest_mac]]
        """
        finalRules = []
        for rule in rules:
            temp = []
            temp.extend(rule[1:])

            finalRules.append(temp)
        return finalRules

def launch():
    core.registerNew(layer2Firewall)
