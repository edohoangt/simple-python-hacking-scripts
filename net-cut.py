import netfilterqueue

def process_packet(packet):
    print(packet)
    packet.drop()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

### Usages ###
# iptables -I FORWARDS -j NFQUEUE --queue-num 0: put forwarding packets (arp spoofed) on queue number 0
# iptables --flush: reset ip table when done