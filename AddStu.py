class AddStu:

    def __init__(self, student_dict):
        self.dict = student_dict 

    def execute(self):      
        name = input("  Please input a student's name or exit: ")
            
        if name != 'exit':
            scores = {} 
            while True:
                subject = input("  Please input a subject name or exit for ending: ")
                if subject == 'exit':
                    break  
                while True:
                    try:
                        score = float(input(f"  Please input {name}'s {subject} score or < 0 for discarding the subject: "))
                        if score < 0:
                            break  
                        scores[subject] = score  
                        break
                    except ValueError as e:
                        print(f'    Wrong format with reason: {e}, try again')

            if scores:  
                self.dict = {"name": name, "scores": scores}

        return self.dict