#!/usr/bin/env python3

import argparse
import subprocess
from termcolor import colored
import signal
import sys
import re

def def_handler(sig, frame):
    print(clored(f"\n[!] Saliendo del programa...", 'red'))
    sys.exit(1)
signal.signal(signal.SIGINT, def_handler)

def get_arguments():
    parser = argparse.ArgumentParser(description="Herramienta para cambiar la direccion MAC de una interfaz de red")
    parser.add_argument("-i", "--interface", required=True, help="Nombre de la interfaz de red")
    parser.add_argument("-m", "--mac", required=True, help="Neva direcion MAC para la interfaz de red")

    return parser.parse_args()

def is_valid_input(interface, mac_address):

    is_valid_interface = re.match(r'^[e][n|t][s|h|p]\d{1}[s]\d{1}$', interface)
    is_valid_mac_address = re.match(r'^([A-Fa-f0-9]{2}[:]{5}[A-Fa-f0-9]{2}$', mac_address)

    return is_valid_interface and is_valid_mac_address

def change_mac_address(interface, mac_address):

    if is_valid_input(interface, mac_address):
        subprocess.run(["ifconfig", interface, "down"])
        subprocess.run(["ifconfig", interface, "hw", "ether", mac_address])
        subprocess.run(["ifconfig", interface, "up"])

        print(colored(f"\n[+] La MAC ha sido cambiada exitosamente\n", 'green'))
    else:
        print(colored(f"\n[!] Los datos ingresados no son correctos\n", 'red'))

def main():
    args = get_arguments()
    change_mac_address(args.interface, args.mac)

if __name__ == '__main__':
    main()

