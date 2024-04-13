class AddStu:
    def __init__(self, connection,student_dict,parameters):
        self.connection = connection
        self.student_dict = student_dict
        self.parameters = parameters

    def execute(self):
        name=self.parameters['name']
        if not(name in self.student_dict): 
            print(self.parameters['scores'])
            print(type(self.student_dict))
            print(type(self.parameters['scores']))
            self.student_dict[name] = self.parameters['scores']
            reply_msg = "Add "+ str(self.parameters) +" success"
            print(reply_msg)
            self.connection.send(reply_msg.encode())
        else:
            reply_msg = f"Add {self.parameters} fail"
            print(reply_msg)
            self.connection.send(reply_msg.encode())
        return self.student_dict