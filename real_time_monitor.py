from scapy.all import sniff

def detect_packet(packet):
    print(packet.summary())  # Can be used to analyze live network packets

sniff(filter="tcp", prn=detect_packet, count=20)  # Capture 20 packets
