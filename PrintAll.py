import json
class PrintAll():
    def __init__(self, server_response):
        if isinstance(server_response, str):
            try:
                self.server_response = json.loads(server_response)
            except json.JSONDecodeError:
                print("Error decoding server response.")
                self.server_response = {}
        elif isinstance(server_response, dict):
            self.server_response = server_response
        else:
            self.server_response = {}

    def execute(self):
        print("\n==== Student List ====")
        parameters = self.server_response.get("parameters")

        for student, info in parameters.items():
            print(f"\nName: {student}")
            for subject, score in info.get("scores", {}).items():
                print(f"  subject: {subject}, score: {score}")
        print("\n======================")
        return