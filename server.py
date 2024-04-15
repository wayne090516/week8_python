from threading import Thread
import socket
import json

host = "127.0.0.1"
port = 20001

class StudentDatabase:
    def __init__(self, data_file):
        self.students = {}
        self.data_file = data_file
        self.load_students()

    def add_student(self, student):
        name = student['name']
        self.students[name] = student
        self.save_students()

    def get_all_students(self):
        return list(self.students.values())

    def save_students(self):
        with open(self.data_file, "w") as file:
            json.dump(list(self.students.values()), file)

    def load_students(self):
        try:
            with open(self.data_file, "r") as file:
                student_list = json.load(file)
                for student in student_list:
                    self.students[student['name']] = student
        except FileNotFoundError:
            pass

class SocketServer(Thread):
    def __init__(self, host, port, data_file):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The following setting is to avoid the server crash. So, the binded address can be reused
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.student_db = StudentDatabase(data_file)

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
        keep_going = True
        while keep_going:
            try:
                message = connection.recv(1024).strip().decode()
            except Exception as e:
                print("Exeption happened {}, {}".format(e, address))
                keep_going = False
            else:
                if not message:
                    keep_going = False
                print("server received:", message, "from", address)
                message = json.loads(message)
                command = message.get('command')
                if command == "show":
                    self.show_students(connection)
                elif command == "add":
                    parameters = message.get('parameters',{})
                    self.add_student(parameters, connection) 
                else:
                    connection.send("Invalid command".encode())
        
        connection.close()
        print("{} close connection".format(address))

    def show_students(self, connection):
        students = self.student_db.get_all_students()        
        response = {'status': 'OK', 'parameters': {student['name']:student for student in  students}}
        connection.send(json.dumps(response).encode())

    def add_student(self, parameters, connection):
        name = parameters.get('name')
        scores = parameters.get('scores', {})
        if name in self.student_db.students:
            response = {'status': 'Fail', 'reason': 'The name already exists.'}
            connection.send(json.dumps(response).encode())
        else:
            self.student_db.add_student({'name': name, 'scores': scores})       
            response = {'status': 'OK'}
            connection.send(json.dumps(response).encode())

if __name__ == '__main__':
    data_file = "student_data.json"
    server = SocketServer(host, port, data_file)
    server.daemon = True
    server.serve()

    # because we set daemon is true, so the main thread has to keep alive
    while True:
        command = input()
        if command == "finish":
            break
    
    server.server_socket.close()
    print("leaving ....... ")
