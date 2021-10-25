#!usr/bin/python

"""
Author: Bruno Sousa

CROCUS TLS

Remove old topology if necessary by using:
sudo mn -c

"""

from mininet.link import TCLink
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSSwitch
from mininet.topo import LinearTopo, Topo
from mininet.clean import cleanup
from mininet.log import info, output, warn, setLogLevel
from mininet.cli import CLI
import time
import random
from myClasses.MyTreeTopo import MyTreeTopo
from myClasses.MyFatTree import MyFatTree
from myClasses.MyLinearTopo import MyLinearTopo
import sys

c1 = RemoteController( 'c1', ip='10.3.3.219', port=6653 )
c2 = RemoteController( 'c2', ip='10.3.3.220', port=6653 )
bwLinkHosts=1000 #consider 1Gbps
bwLinkSwitches=1000     # consider 10Gbps   NOW WITH 1Gbps
nFailures=1
timeFailure = 10 #random.randint(30,60) # failure between 30 and 60
timeBetweenFailues = 2 #random.randint(0,2) # failure bellow 2s  
idHostsFail =  [0,1,2,3,4,5]  # the first hosts failing



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
        net = Mininet(mytopo, switch=OVSSwitch, controller=None, autoSetMacs=True, ipBase='192.168.1.0/24' )
        
        net.addController(c1)
        net.addController(c2)
        net.start()
    
        net.pingAll()
        doFailure(net.hosts)
        net.pingAll()
        time.sleep(5)
    
        net.stop()
    except Exception:
        print('Error occurred')



def linear_topo(iSwitches=2, iHosts=24):
    print(' Linear topology switches='+ str(iSwitches) + ' hosts=' + str(iHosts) )
    
    try:
        mytopo = MyLinearTopo(k=iSwitches, n=iHosts, bwHosts=bwLinkHosts, bwSwitches=bwLinkHosts)
        #mtopo = LinearTopo(k=iSwitches, n=iHosts, protocols='OpenFlow13')
        net = Mininet(mytopo, switch=OVSSwitch, controller=None, autoSetMacs=True, ipBase='192.168.1.0/24')
        #print( '*** Adding controllers' )
        net.addController(c1)
        net.addController(c2)
        #net.build()
        net.start()
        
        net.pingAll()
        doFailure(net.hosts)
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
        net.pingAll()
        time.sleep(5)

        net.stop() 

    except Exception:
        print('Error occurred')

if __name__ == '__main__':
    setLogLevel( 'info' )
    cleanup()
    if len(sys.argv) > 1:
        opt = int(sys.argv[1])
        print(opt)
        if opt == 0:
            linear_topo(4,2) # GEANT    
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
    
        