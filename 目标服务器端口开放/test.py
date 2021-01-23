import os
import socket
def is_tcp_connection_open(target_ip, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    success = True
    try:
        sock.connect((target_ip, target_port))
        print('connect to ip %s port %d ok' %(target_ip, target_port))
    except Exception as e:
        success = False
        print('connect to ip %s port %d ok' %(target_ip, target_port))
    finally:
        sock.close()
    return success
print is_tcp_connection_open("10.50.21.115", 443)

