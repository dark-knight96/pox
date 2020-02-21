#custom component

from pox.core import core
import pox.lib.packet as pkt 
from pox.lib.util import dpid_to_str as sc
import pox.openflow.libopenflow_01 as of

#Gets logger.
log = core.getLogger()


class layer2Firewall(object):
    def __init__(self):
        core.openflow.addListeners(self)
        log.debug("Starting this component") 
    def _handle_ConnectionUp(self, event):
        #using ofp_match attributes
        connection = event.connection 
        log.debug("****CONNECTION UP*****")
        log.debug("packet received from " + sc(event.dpid))
        log.debug(connection)
    def _handle_PacketIn(self, event):
        log.debug("Packet in message!!")
        log.debug("packet received from " + sc(event.dpid))

def launch():
    core.registerNew(custom)
