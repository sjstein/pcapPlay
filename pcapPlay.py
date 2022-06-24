import argparse
import os
import socket
import struct
import sys
import time

from scapy.utils import RawPcapReader

HDR_LEN = 42    # 42 bytes of packet info before data payload.
                # No need to send those here as the Python socket library handles packet construction.

def process_pcap(file_name):
    # Set up the multicast datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    # Open file and send out packets
    count = 0
    for pkt_data, pkt_meta_data in RawPcapReader(file_name):
        sock.sendto(pkt_data[HDR_LEN:], multicast_group)
        count += 1
        time.sleep(pckt_delay / 100000)
    #print(f'Sent {count} packets')
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PCAP reader')
    parser.add_argument('filename', help='pcap file to parse')
    parser.add_argument('-d', '--delay', help='delay between packets sent (in microseconds) [50].',
                        default=50)
    parser.add_argument('-i', '--ipaddr', help='Specify multicast address [239.255.50.10]',
                        default='239.255.50.10')
    parser.add_argument('-p', '--port', help='Specify multicast port [5010]',
                        default=5010)
    parser.add_argument('-r', '--repeat', help='Number of times to run through packets (0 = nonstop) [1]',
                        default=1)
    args = parser.parse_args()
    file_name = args.filename
    pckt_delay = int(args.delay)
    rep = int(args.repeat)
    multicast_group = (args.ipaddr, int(args.port))

    if not os.path.isfile(file_name):
        print(f'{file_name} does not exist.', file=sys.stderr)
        sys.exit(-1)
    print(f'Opening {file_name}')
    if rep == 0:
        while True:
            process_pcap(file_name)
    else:
        for i in range(1, rep+1):
            print(f'Sent {process_pcap(file_name)} packets from {file_name} : iteration {i}')
            time.sleep(pckt_delay / 100000)

    sys.exit(0)
