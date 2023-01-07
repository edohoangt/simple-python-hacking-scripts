import scapy.all as scapy
import argparse

def scan(ip):
    arp_req = scapy.ARP(pdst=ip)
    # print(arp_req.summary())
    # arp_req.show()

    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # print(broadcast.summary())
    # broadcast.show()

    arp_req_brdcast = broadcast / arp_req
    # print(arp_req_brdcast.summary())
    # arp_req_brdcast.show()

    answered_list = scapy.srp(arp_req_brdcast, timeout=1, verbose=False)[0] # send and received pkts with custom ether part
    print(answered_list.summary())

    print("IP\t\t\tMAC Address\n--------------------------")
    for elem in answered_list:
        print(elem[1].psrc + "\t" + elem[1].hwsrc)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range.")
    args = parser.parse_args()
    return args

args = get_arguments()
# scan("192.168.21.1/24")
scan(args.target)

### USAGE ###
# python network_scanner.py --t 10.0.2.1/24
# python network_scanner.py --target 10.0.2.1/24