from mininet.link import TCLink
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel

'''
mn --custom lab3topo.py --topo mytopo --controller=remote,ip=127.0.0.1,port=6653 --switch ovs,protocols=OpenFlow13 --arp --mac

'''


class lab3topo(Topo):
    # ---------------------------------- set k value-----------------------------------
    def __init__(self, *args, **opts):

        super().__init__(*args, **opts)
        s1 = self.addSwitch('s1', cls=OVSKernelSwitch, dpid='000000000001')  # add switch1
        s2 = self.addSwitch('s2', cls=OVSKernelSwitch, dpid='000000000002')  # add switch2
        s3 = self.addSwitch('s3', cls=OVSKernelSwitch, dpid='000000000003')  # add switch3
        s4 = self.addSwitch('s4', cls=OVSKernelSwitch, dpid='000000000004')  # add switch4
        s5 = self.addSwitch('s5', cls=OVSKernelSwitch, dpid='000000000005')  # add switch5

        h1 = self.addHost('h1', ip='10.0.0.1')  # add host1
        h2 = self.addHost('h2', ip='10.0.0.2')  # add host2

        self.addLink(h1, s1, 0, 1)  # add link h1:0 <---> s1:1
        self.addLink(h2, s5, 0, 1)  # add link h2:0 <---> s5:1
        self.addLink(s1, s2, 2, 1)  # add link s1:2 <---> s2:1
        self.addLink(s1, s3, 3, 1)  # add link s1:3 <---> s3:1
        self.addLink(s1, s4, 4, 1)  # add link s1:4 <---> s4:1
        self.addLink(s5, s2, 2, 2)  # add link s5:2 <---> s2:2
        self.addLink(s5, s3, 3, 2)  # add link s5:3 <---> s3:2
        self.addLink(s5, s4, 4, 2)  # add link s5:4 <---> s4:2

        print('topo created')


TOPOS = {'mytopo': (lambda: lab3topo())}
