#!/usr/bin/env python
import time
from datetime import datetime
import socket
import sys
import struct
import argparse
import logging

logger = logging.getLogger('mctest')

group = '232.8.8.8'
MCAST_PORT = 7878
mttl = 6
message = 'multicast test tool'

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='Multicast Send/Receive Test Tool')
parser.add_argument("-send", metavar="string", help="Send a Message",
                    type=str)
parser.add_argument("-receive", help="Receive Messages from Group",
                    action="store_true")
parser.add_argument("-group", metavar="Multicast Group (default: 232.8.8.8", type=str)
parser.add_argument('-ttl', metavar='int', help="Multicast TTL (default 4)", type=int)
parser.add_argument("-v", help="Verbose Output", action="store_true")
args = parser.parse_args()

def receiver(group):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
                                # to MCAST_GRP, not all groups on MCAST_PORT
    mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        print ('Received from ' + group + ': ' + sock.recv(1024))


def sender(group):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, mttl, 2)
    while 1:
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mcast_msg = message + ': ' + time_now
        print('Sending to ' + group + ' (TTL ' + str(mttl) + '): ' + mcast_msg)
        sock.sendto(mcast_msg, (group, MCAST_PORT))
        time.sleep(1)

if args.group:
    group = args.group
if args.ttl:
    mttl = args.ttl

if args.send:
    message = args.send
    sender(group)
elif args.receive:
    receiver(group)
else:
    parser.print_help()