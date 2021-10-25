# Credits to: Pandr
# source: https://github.com/panandr/mininet-fattree/blob/master/fattree.py
#
from mininet.topo import Topo
from mininet.net import Mininet


class MyFatTree(Topo):
    CoreSwitchList = []
    AggSwitchList = []
    EdgeSwitchList = []
    HostList = []
 
    def __init__( self, k, bwLinkSwitches, bwLinkHosts):
        " Create Fat Tree topo."
        self.pod = k
        self.iCoreLayerSwitch = (k/2)**2
        self.iAggLayerSwitch = k*k/2
        self.iEdgeLayerSwitch = k*k/2
        self.density = k/2
        self.iHost = self.iEdgeLayerSwitch * self.density
        
        self.bw_c2a = bwLinkSwitches
        self.bw_a2e = bwLinkSwitches
        self.bw_h2a = bwLinkHosts

        # Init Topo
        Topo.__init__(self)
        self.createTopo()
        self.createLink( bw_c2a=self.bw_c2a, 
                         bw_a2e=self.bw_a2e, 
                         bw_h2a=self.bw_h2a)
        #return Mininet( self, **kwargs )

    
    def createTopo(self):
        self.createCoreLayerSwitch(self.iCoreLayerSwitch)
        self.createAggLayerSwitch(self.iAggLayerSwitch)
        self.createEdgeLayerSwitch(self.iEdgeLayerSwitch)
        self.createHost(self.iHost)

    """
    Create Switch and Host
    """
    def _addSwitch(self, number, level, switch_list):
        for x in range(1, int(number)+1):
            PREFIX = str(level) + "00"
            if x >= int(10):
                PREFIX = str(level) + "0"
            switch_list.append(self.addSwitch('s' + PREFIX + str(x), protocols='OpenFlow13'))

    def createCoreLayerSwitch(self, NUMBER):
        self._addSwitch(NUMBER, 1, self.CoreSwitchList)

    def createAggLayerSwitch(self, NUMBER):
        self._addSwitch(NUMBER, 2, self.AggSwitchList)

    def createEdgeLayerSwitch(self, NUMBER):
        self._addSwitch(NUMBER, 3, self.EdgeSwitchList)

    def createHost(self, NUMBER):
        for x in range(1, int(NUMBER)+1):
            PREFIX = "h00"
            if x >= int(10):
                PREFIX = "h0"
            elif x >= int(100):
                PREFIX = "h"
            self.HostList.append(self.addHost(PREFIX + str(x)))

    """
    Add Link
    """
    def createLink(self, bw_c2a=0.2, bw_a2e=0.1, bw_h2a=0.5):
        end = self.pod//2 # Integer division
        for x in range(0, int(self.iAggLayerSwitch), end):
            for i in range(0, end):
                for j in range(0, end):
                    linkopts = dict(bw=bw_c2a) 
                    self.addLink(
                        self.CoreSwitchList[i*end+j],
                        self.AggSwitchList[x+i],
                        **linkopts)

        for x in range(0, int(self.iAggLayerSwitch), end):
            for i in range(0, end):
                for j in range(0, end):
                    linkopts = dict(bw=bw_a2e) 
                    self.addLink(
                        self.AggSwitchList[x+i], self.EdgeSwitchList[x+j],
                        **linkopts)

        for x in range(0, int(self.iEdgeLayerSwitch)):
            for i in range(0, int(self.density)):
                linkopts = dict(bw=bw_h2a) 
                self.addLink(
                    self.EdgeSwitchList[x],
                    self.HostList[int(self.density) * x + i],
                    **linkopts)



