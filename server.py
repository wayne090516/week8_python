from threading import Thread
import socket
from StudentInfoProcessor import StudentInfoProcessor
from AddStu import AddStu
from PrintAll import PrintAll

host = "127.0.0.1"
port = 20001

action_list = {
    "add": AddStu, 
    "show": PrintAll
}

class SocketServer(Thread):
    def __init__(self, host, port, student_dict):
        super().__init__()
        self.student_dict = student_dict
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The following setting is to avoid the server crash. So, the binded address can be reused
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)

    def serve(self):
        self.start()

    def run(self):
        while True :
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
                message = eval(message)
                if message['command'] == "close":
                    connection.send("closing".encode())
                    keep_going = False
                else:
                    parameters = message['parameters']
                    command = message['command']
                    self.student_dict = action_list[command](connection, self.student_dict, parameters).execute()
                    
        connection.close()
        print("{} close connection".format(address))

    def stop(self):   
        self.server_socket.close()

if __name__ == '__main__':
    student_dict = StudentInfoProcessor().read_student_file()
    server = SocketServer(host, port ,student_dict)
    server.daemon = True
    server.serve()

    while True:
        command = input()
        if command == "finish":
            break
    
    server.stop()
    server.join()
    print("leaving ....... ")
    StudentInfoProcessor().restore_student_file(student_dict)