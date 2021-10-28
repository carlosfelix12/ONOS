from mininet.topo import Topo
from mininet.net import Mininet

class MyTLSLinearTopo(Topo):
    "Linear topology of k switches, with n hosts per switch."
    def __init__(self,k, n, bwHosts, bwSwitches):
        self.k = k
        self.n = n
        self.bwHosts = bwHosts
        self.bwSwitches = bwSwitches
        self.strCmd='ovs-vsctl set-controller s1 ssl:10.3.1.203:6653'
        Topo.__init__(self)
        self.switchNum=0
        self.addLinear()
        #return Mininet(self, switch=OVSSwitch,controller=None )
        
    def addLinear(self):
        linkopts=dict(bw=self.bwHosts)
        if self.n == 1:
            genHostName = lambda i, j: 'h%s' % i
        else:
            genHostName = lambda i, j: 'h%ss%d' % ( j, i )

        lastSwitch = None
        for i in range( 0, int(self.k) ):
            # Add switch
            self.switchNum += 1
            switch = self.addSwitch( 's%s' % self.switchNum, protocols='OpenFlow13' )

            # Add hosts to switch
            for j in range( 0, int(self.n) ):
                host = self.addHost( genHostName( self.switchNum, j ) )
                linkopts=dict(bw=self.bwHosts)
                self.addLink( host, switch, **linkopts )
            # Connect switch to previous
            if lastSwitch:
                linkopts=dict(bw=self.bwSwitches)
                self.addLink( switch, lastSwitch, **linkopts )
            #switch.cmd(self.strCmd) # Set controller
            lastSwitch = switch

