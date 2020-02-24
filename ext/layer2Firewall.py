#Simple layer 2 firewall

from pox.core import core
import sqlmanager as sql
from pox.lib.revent import *
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import EthAddr

log = core.getLogger()

class layer2Firewall(EventMixin):
    def __init__(self):
        self.rules = utilMethods.getOnlyRules(utilMethods.getFireWallRules())
        log.debug("Firewall rules loaded")
        self.listenTo(core.openflow)
        log.debug("Starting layer2Firewall")
        log.debud(self.rules)

    def _handle_ConnectionUp(self, event):
        for rule in self.rules():
            matchInstance = of.ofp_match()
            matchInstance.dl_src = EthAddr(rule[0])
            matchInstance.dl_dst = EthAddr(rule[1])

            #Sending new flow mod message
            flowMod = of.ofp_flow_mod()
            flowMod.match = matchInstance
            event.connection.send(flowMod)

class utilMethods():
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
