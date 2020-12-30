import socket
import struct
import sys
import pickle

from cluster import hosts, ports

message = 'I am a new Server'
mutlicast_address = ('224.3.29.71', ports.multicast)
buffer_size = 1024
unicode = 'utf-8'

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the timeout so the socket does not block indefinitely when trying to receiver data
sock.settimeout(0.5)

# Set the time-to-live for messages to 1 so they do not go past the local network segment
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)


def update_server_list():
    while True:
        try:
            sock.sendto(message.encode('utf-8'), mutlicast_address)
            data = sock.recvfrom(buffer_size)[0]
            print(f'[MULTICAST SENDER {hosts.myIP}] Multicast Receiver sends the Server list',
                  file=sys.stderr)
            hosts.server_list = pickle.loads(data)
            print(f'[MULTICAST SENDER {hosts.myIP}] Server list UPDATED',
                  file=sys.stderr)
            break
        except socket.timeout:
            print('FAIL')


def sending_request_to_multicast():
    try:
        # Send data to the Multicast address
        print(f'\n[MULTICAST SENDER {hosts.myIP}] Starting UDP Socket and sending data to Multicast Receiver {mutlicast_address}',
              file=sys.stderr)
        sock.sendto(message.encode('utf-8'), mutlicast_address)

        # Look for responses from all recipients
        while True:
            try:
                data, server = sock.recvfrom(buffer_size)
                if len(data) > 15:
                    print(f'[MULTICAST SENDER {hosts.myIP}] Multicast Receiver sends the Server list',
                          file=sys.stderr)
                    hosts.server_list = pickle.loads(data)
                    print(f'[MULTICAST SENDER {hosts.myIP}] Server list UPDATED',
                          file=sys.stderr)
                else:
                    print(f'[MULTICAST SENDER {hosts.myIP}] Multicast Receiver response with --{data.decode(unicode)}-- from {server}',
                          file=sys.stderr)
                return True
            except socket.timeout:
                print(f'[MULTICAST SENDER {hosts.myIP}] Multicast Receiver not detected',
                      file=sys.stderr)
                return False
    except Exception as e:
        print(f'[MULTICAST SENDER {hosts.myIP}] {e}',
              file=sys.stderr)
