
class PK_SimpleOperator:
    def __init(self, poll=None, execute=None):
        self.poll = poll
        self.execute = execute

    def __call__(self):
        if self.poll != None and self.poll():
            self.execute()
