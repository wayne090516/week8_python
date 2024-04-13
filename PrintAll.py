class PrintAll:
    def __init__(self, connection, student_dict, parameters):
        self.connection = connection
        self.student_dict = student_dict
        self.parameters = parameters

    def execute(self):
        reply_msg = "{'status': 'OK', 'parameters': "+str(self.student_dict) +"}"
        self.connection.send(reply_msg.encode())
        return self.student_dict