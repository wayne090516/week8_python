class ServerAddStu:

    def __init__(self, data_center, parameters):
        self.data_center = data_center
        self.parameters = parameters
        self.executed_data = {}

    def execute(self):
        if self.parameters['name'] in self.data_center:
            self.executed_data['status'] = 'Fail'
            self.executed_data['reason'] = "The name already exists."
        else:
            self.executed_data['status'] = 'OK' 
            self.data_center[self.parameters['name']] = self.parameters

        return self.executed_data, self.data_center