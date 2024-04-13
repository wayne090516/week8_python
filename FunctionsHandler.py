class FunctionsHandler:
    def __init__(self):
        self.students = {}

    def add_student(self, parameters):
        student_name = parameters.get('name')
        student_scores = parameters.get('scores', {})

        if student_name in self.students:
            return {'error': f'Student {student_name} already exists'}

        self.students[student_name] = student_scores
        return {'success': f'Student {student_name} added successfully'}

    def show_students(self):
        if not self.students:
            return {'parameters': {}}

        parameters = {}
        for student, scores in self.students.items():
            parameters[student] = {'scores': scores}

        return {'parameters': parameters}

    def command_handler(self, message):
        command = message['command']
        parameters = message['parameters']

        if command == 'add':
            result = self.add_student(parameters)
            return result
        elif command == 'show':
            result = self.show_students()
            return result
        else:
            return {'error': 'Invalid command'}