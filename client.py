import socket 
import json
from AddStu import AddStu
from PrintAll import PrintAll

host = "127.0.0.1"
port = 20001 
BUFFER_SIZE = 1940

class SocketClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.client_socket.connect((host, port))

    def send_command(self, command, parameters):
        send_data = {"command": command, "parameters": parameters}
        print(f"The client sent data => {send_data}")
        self.client_socket.send(json.dumps(send_data).encode())

    def wait_response(self):
            data = self.client_socket.recv(BUFFER_SIZE)
            raw_data = data.decode()
            keep_going = True

            if raw_data == "closing":
                keep_going = False
            else:
                raw_data = json.loads(raw_data)
            print(f"The client received data => {raw_data}")
            return keep_going, raw_data

class StudentClientHandler:
    def __init__(self, client):
        self.client = client

    def add_student(self):
        parameters = AddStu(client).execute()
        self.client.send_command('add', parameters)
        return self.client.wait_response()[0]

    def show_students(self):
        self.client.send_command('show', { })
        keep_going, response = self.client.wait_response()
        PrintAll(response).execute()
        return keep_going

    def exit_program(self):
        self.client.send_command('exit',{})
        return False

    def default_behavior(self):
        print("Unknown selection.")
        return True
        
def input_choice():
    choice=input("add: Add a student's name and score\nshow: Print all\nexit: Exit\nPlease select: ")
    return choice

if __name__ == '__main__':
    client = SocketClient(host, port)
    handler = StudentClientHandler(client)
    actions = {
        'add': handler.add_student,
        'show': handler.show_students,
        'exit': handler.exit_program,
    }

    try:
        while True:
            user_choice = input_choice()
            keep_going = actions.get(user_choice, handler.default_behavior)()
            if not keep_going:
                break
    except Exception as e:
        print(f"An error occurred: {e}")