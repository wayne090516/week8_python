class ServerPrintAll:

    def __init__(self, data_center, parameters):
        self.data_center = data_center
        # self.parameters = parameters #no use here
        self.executed_data = {}

    def execute(self):
        if isinstance(self.data_center, dict):
            self.executed_data['status'] = 'OK'
            self.executed_data['parameters'] = self.data_center
        else:
            self.executed_data['status'] = 'Fail'
            self.executed_data['reason'] = "Data isn't in the right format."

        return self.executed_data, self.data_center