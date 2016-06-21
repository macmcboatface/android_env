#!/home/mac/Desktop/env/.virtualenv/bin/python
import sys

import socket

def send_file_over_udp(filename, offset):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ("127.0.0.1", 6666)

    with open(filename) as h:
        data = h.read()
        sock.sendto(data[offset:], addr)

if __name__ == "__main__":
    filename = sys.argv[1]
    offset = int(sys.argv[2])
    send_file_over_udp(filename, offset)


