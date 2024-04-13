from threading import Thread
from ServerAddStu import ServerAddStu
from ServerPrintAll import ServerPrintAll
import socket
import json

host = "127.0.0.1"
port = 20001
action_list = {
    "add": ServerAddStu,  
    "show": ServerPrintAll
}

class SocketServer(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The following setting is to avoid the server crash. So, the binded address can be reused
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.data_center = {} #store all student data

    def serve(self):
        self.start()

    def run(self):
        while True:
            connection, address = self.server_socket.accept()
            print("{} connected".format(address))
            self.new_connection(connection=connection, address=address)

    def new_connection(self, connection, address):
        Thread(target=self.receive_message_from_client,
                                kwargs={"connection": connection, "address": address}, daemon=True).start()

    def receive_message_from_client(self, connection, address):
        keep_going = True
        while keep_going:
            try:
                message = connection.recv(1024).strip().decode()
            except Exception as e:
                print("Exeption happened {}, {}".format(e, address))
                keep_going = False
            else:
                if not message:
                    break
                message = json.loads(message)
                if message['command'] == "exit":
                    connection.send("closing".encode())
                    keep_going = False
                else:
                    #recieve and execute commands
                    print(message)
                    print("    server received:{}from{}".format(message,address))
                    executed_data, self.data_center = DataController(message, self.data_center).execute()
                    reply_msg = json.dumps(executed_data)
                    connection.send(reply_msg.encode())
        
        connection.close()
        print("{} close connection".format(address))

class DataController():
    def __init__(self, message, data_center):
        self.client_data = message
        self.command = ""
        self.parameters = {}
        self.executed_data = {}
        self.data_center = data_center

    def execute(self):
        self.command = self.client_data['command']
        self.parameters = self.client_data['parameters']
        self.executed_data, self.data_center = action_list[self.command](self.data_center ,self.parameters).execute()

        return self.executed_data, self.data_center

if __name__ == '__main__':
    server = SocketServer(host, port)
    server.daemon = True
    server.serve()

    # because we set daemon is true, so the main thread has to keep alive
    while True:
        command = input()
        if command == "finish":
            break
    
    server.server_socket.close()
    print("leaving ....... ")
