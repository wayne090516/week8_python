from threading import Thread
import socket
import json

host = "127.0.0.1"
port = 20001

class SocketServer(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.students = {}

    def serve(self):
        self.start()

    def run(self):
        while True:
            connection, address = self.server_socket.accept()
            print("{} connected".format(address))
            self.new_connection(connection=connection,
                                address=address)

    def new_connection(self, connection, address):
        Thread(target=self.receive_message_from_client,
               kwargs={
                   "connection": connection,
                   "address": address}, daemon=True).start()
        
    def receive_message_from_client(self, connection, address):
        keepgoing = True
        while keepgoing == True:
            data = connection.recv(1024).decode()
            if not data:
                break
            try:
                message = json.loads(data)
                command = message.get('command')
                parameters = message.get('parameters')
                if command == "add":
                    Function().add_student(parameters, connection, address, self.students, data)
                elif command == "show":
                    Function().show_student(connection, data, address, self.students)
                elif command == "exit":
                    Function().exit(address)
                    keepgoing = False
                else:
                    print("Unknown command")
            except json.JSONDecodeError:
                connection.send(json.dumps({"status": "Invalid JSON"}).encode())
            except Exception as e:
                connection.send(json.dumps({"status": "Error", "message": str(e)}).encode())
        connection.close()

class Function:
    @staticmethod
    def add_student(parameters, connection, address, students, data):
        print(data)
        student_name = parameters['name']
        if student_name in students:
            print("Name already exists:", student_name)
            reply_msg = json.dumps({'status': 'Fail', 'reason': 'The name already exists.'})
            connection.send(reply_msg.encode())
            return
        students[student_name] = parameters
        print("Server received:", parameters, "from", address)
        reply_msg = json.dumps({'status': 'OK'})
        connection.send(reply_msg.encode())

    @staticmethod
    def show_student(connection, data, address, students):
        print(data)
        print("server received:", data, "from", address)
        reply_msg = json.dumps({'status': 'OK', 'parameters': students})
        connection.send(reply_msg.encode())

    @staticmethod
    def exit(address):
        print(f"{address} close connection")

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
