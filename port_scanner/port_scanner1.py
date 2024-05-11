#!/usr/bin/env python3

import socket
from termcolor import colored

host = input(f"\n[+] Itroduce la direccion IP: ")

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    return s 

def port_scanner(port, host, s):

    try:
        s.connect((host, port))
        print(colored(f"\n[+] El puerto {port} esta abierto", 'green'))
        s.close()

    except (socket.timeout, ConnectionRefusedError):
        s.close()

def main():
    
    target = get_arguments()

    for port in range(1,500):
        s = create_socket()
        port_scanner(port, target, s)

if __name__ == '__main__':
    main()
