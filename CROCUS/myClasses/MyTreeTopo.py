from mininet.topo import Topo
from mininet.net import Mininet

# From official class TreeNet but with minos modif for cls link
#
class MyTreeTopo( Topo ):
    "Topology for a tree network with a given depth and fanout."
    def __init__(self, depth, fanout, bwHosts, bwSwitches):
        # Build topology
        self.hostNum=0
        self.bwHosts = bwHosts
        self.bwSwitches = bwSwitches

        Topo.__init__(self)
        self.switchNum=0
        self.addTree( depth, fanout )
        #return Mininet( self, **_opts )

    def addTree( self, depth, fanout ):
        """Add a subtree starting with node n.
           returns: last node added"""
        linkopts = dict(bw=self.bwHosts)
        isSwitch = depth > 0
        if isSwitch:
            
            node = self.addSwitch( 's%s' % self.switchNum, protocols='OpenFlow13' )
            self.switchNum += 1
            for _ in range( fanout ):
                child = self.addTree( depth - 1, fanout )
                self.addLink( node, child, **linkopts )
        else:
            node = self.addHost( 'h%s' % self.hostNum )
            self.hostNum += 1
        return node
