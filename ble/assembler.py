import json


class JsonAssembler:

    def __init__(self):
        self.buffer = ""

    def feed(self, chunk: str):

        self.buffer += chunk

        try:
            obj = json.loads(self.buffer)

            self.buffer = ""

            return obj

        except json.JSONDecodeError:
            return None

    def reset(self):
        self.buffer = ""