#Simple layer 2 firewall

from pox.core import core
import sqlmanager as sql
from pox.lib.revent import *
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import EthAddr


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

            #Sending new flow mod message
            flowMod = of.ofp_flow_mod()
            flowMod.match = matchInstance
            event.connection.send(flowMod)
        from pox.listener import updateBootCore #deferring circular imports
        updateBootCore()

class utilMethods():
    @staticmethod
    def constructmatchStructure(rule):
        match = of.ofp_match()
        match.dl_src = EthAddr(rule[0])
        match.dl_dst = EthAddr(rule[1])

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
            temp.append(str(rule[1]))
            temp.append(str(rule[2]))
            finalRules.append(temp)
        return finalRules

def launch():
    core.registerNew(layer2Firewall)
