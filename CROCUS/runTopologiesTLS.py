#!usr/bin/python

"""
Author: Bruno Sousa

CROCUS TLS

Remove old topology if necessary by using:
sudo mn -c

"""

from mininet.link import TCLink
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSSwitch, OVSController
from mininet.topo import LinearTopo, Topo
from mininet.clean import cleanup
from mininet.log import info, output, warn, setLogLevel
from mininet.cli import CLI
import time
import random
from myClasses.MyTreeTopo import MyTreeTopo
from myClasses.MyFatTree import MyFatTree
from myClasses.MyLinearTopo import MyLinearTopo
from myClasses.MyTLSLinearTopo import MyTLSLinearTopo
import sys

c1 = RemoteController( 'c1', ip='10.3.1.203', port=6653 )
c2 = RemoteController( 'c2', ip='10.3.1.160', port=6653 )
bwLinkHosts=1000 #consider 1Gbps
bwLinkSwitches=1000     # consider 10Gbps   NOW WITH 1Gbps
nFailures=1
timeFailure = 10 #random.randint(30,60) # failure between 30 and 60
timeBetweenFailues = 2 #random.randint(0,2) # failure bellow 2s  
idHostsFail =  [0,1,2,3,4,5]  # the first hosts failing
hostsToPing = ['h0s1','h0s2','h0s3','h0s4','h1s1','h1s2','h1s3','h1s4']


def printConnections( switches ):
    "Compactly print connected nodes to each switch"
    for sw in switches:
        output( '%s: ' % sw )
        for intf in sw.intfList():
            link = intf.link
            if link:
                intf1, intf2 = link.intf1, link.intf2
                remote = intf1 if intf1.node != sw else intf2
                output( '%s(%s) ' % ( remote.node, sw.ports[ intf ] ) )
        output( '\n' )

def printHosts( hosts ):
    for h in hosts:
        output('%s: %s: %s' % (h, h.MAC(), h.IP() ) )
        output('\n')

def doFailure( hosts):
    print ('starting failure')
    time.sleep(5)
    tBegin = time.time()
    tIni = tBegin
    dif =0
    j=0
    nfail=0
    i=0
    while (nfail<=nFailures):
        tNow = time.time()
        dif = tNow-tBegin
        if(dif>=timeFailure ):
            nfail+=1
            tBegin=time.time()
            for h in hosts:
                if i in idHostsFail:
                    #Fail host
                    h.stop(deleteIntfs =True) # Stop and delete interfaces
                    print("failure=" + str(nfail) + " host=" + str(i) + " " + str(tNow) + " " + str(dif) + " " + str(tNow - tBegin ))            
                    time.sleep(timeBetweenFailues)
                i+=1

    print('Ending failures')

def tree_topo(idepth=1, ifanout=2):
    try:
        print(' Tree topology d='+ str(idepth) + ' fan=' + str(ifanout) )
        mytopo = MyTreeTopo(depth=idepth, fanout=ifanout, bwHosts=bwLinkHosts, bwSwitches=bwLinkHosts)
        net = Mininet(mytopo, switch=OVSSwitch, controller=None, autoSetMacs=True, ipBase='192.168.1.0/16' )
        
        net.addController(c1)
        net.addController(c2)
        net.start()
    
        net.pingAll()
        doFailure(net.hosts)
        time.sleep(1)
        net.pingAll()
        time.sleep(5)
    
        net.stop()
    except Exception:
        print('Error occurred')



def linear_topo(iSwitches=2, iHosts=24):
    print(' Linear topology switches='+ str(iSwitches) + ' hosts=' + str(iHosts) )
    
    try:
        mytopo = MyLinearTopo(k=iSwitches, n=iHosts, bwHosts=bwLinkHosts, bwSwitches=bwLinkHosts)
        net = Mininet(mytopo, switch=OVSSwitch, controller=None, autoSetMacs=True, ipBase='192.168.1.0/16')
        net.addController(c1)
        net.addController(c2)
        
        net.start()
        
        net.pingAll()
        doFailure(net.hosts)
        time.sleep(1)
        net.pingAll()
        time.sleep(5)

        net.stop()
    except Exception as e:
        print('Error occurred')
        print (format(e))


def fatTree(iK=12):
    try:
        mytopo=MyFatTree(iK,bwLinkSwitches,bwLinkHosts)    
        net = Mininet(mytopo, switch=OVSSwitch, controller=None, autoSetMacs=True, ipBase='192.168.1.0/24')

        net.addController(c1)
        net.addController(c2)
        net.start()

        net.pingAll()
        doFailure(net.hosts)
        time.sleep(1)
        net.pingAll()
        time.sleep(5)

        net.stop() 
    except Exception:
        print('Error occurred')


def linear_topo_TLS(iSwitches=2, iHosts=24):
    print(' Linear topology with TLS switches='+ str(iSwitches) + ' hosts=' + str(iHosts) )
    

    try:
        switchNum=0
        nSwitch=0
        #mytopo = MyTLSLinearTopo(k=iSwitches, n=iHosts, bwHosts=bwLinkHosts, bwSwitches=bwLinkHosts)
        net = Mininet(switch=OVSSwitch, controller=OVSController, autoSetMacs=True, ipBase='192.168.1.0/16')
        #net.addController(c1)

        lastSwitch = None
        if iHosts == 1:
            genHostName = lambda i, j: 'h%s' % i
        else:
            genHostName = lambda i, j: 'h%ss%d' % ( j, i )

        for i in range( 0, int(iSwitches) ):
            # Add switch
            switchNum += 1
            switch = net.addSwitch( 's%s' % switchNum, protocols='OpenFlow13' )

            # Add hosts to switch
            for j in range( 0, int(iHosts) ):
                host = net.addHost( genHostName( switchNum, j ) )
                linkopts=dict(bw=bwLinkHosts)
                net.addLink( host, switch, **linkopts )
            # Connect switch to previous
            if lastSwitch:
                linkopts=dict(bw=bwLinkHosts)
                net.addLink( switch, lastSwitch, **linkopts )
            #switch.cmd(self.strCmd) # Set controller
            lastSwitch = switch
      
        net.start()
        for i in range( 1, int(iSwitches) +1 ):
            swiNode=net.getNodeByName('s%s' % i)
            swiName='s%s' % i 
            print (swiName)
            swiNode.cmd('ovs-vsctl set-controller '+ swiName +' ssl:10.3.1.203:6653')
        #s2.cmd('ovs-vsctl set-controller s2 ssl:10.3.1.203:6653')
        #s3.cmd('ovs-vsctl set-controller s3 ssl:10.3.1.203:6653')
        #s4.cmd('ovs-vsctl set-controller s4 ssl:10.3.1.203:6653')

        net.pingAll()
        #doFailure(net.hosts)
        #time.sleep(1)
        #net.pingAll()
        time.sleep(5)
        net.interact()
        #net.stop()
    except Exception as e:
        print('Error occurred')
        print (format(e))

if __name__ == '__main__':
    setLogLevel( 'info' )
    cleanup()
    if len(sys.argv) > 1:
        opt = int(sys.argv[1])
        print(opt)
        if opt == 0:
            linear_topo_TLS(4,64) 
            #linear_topo(4,64) # GEANT, considering Pica8 capabilities # total of 256 hosts
        elif opt == 1:
            tree_topo(4,4)    
        elif opt == 2:
            tree_topo(7,2)
        elif opt == 3:
            linear_topo(100, 24)
        elif opt == 4:
            fatTree(12) # 12 pods
            #fatTree(2)
        else:
            print('Wrong test ID')
    else:
        print('No given ID for test')
    
        