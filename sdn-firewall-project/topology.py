from mininet.topo import Topo

class FirewallTopo(Topo):
    def build(self):
        # Add one switch
        s1 = self.addSwitch('s1')

        # Add three hosts
        h1 = self.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/24')
        h2 = self.addHost('h2', mac='00:00:00:00:00:02', ip='10.0.0.2/24')
        h3 = self.addHost('h3', mac='00:00:00:00:00:03', ip='10.0.0.3/24')

        # Connect each host to switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)

topos = {'firewalltopo': (lambda: FirewallTopo())}
