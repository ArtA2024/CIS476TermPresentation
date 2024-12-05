class Step:
    def __init__(self, next_step=None):
        self.next_step = next_step

    def handle(self, user, answer):
        if self.next_step:
            return self.next_step.handle(user, answer)
        return True

class Question1Step(Step):
    def handle(self, user, answer):
        if user.security_a1.lower() != answer.lower():
            return False
        return super().handle(user, answer)

class Question2Step(Step):
    def handle(self, user, answer):
        if user.security_a2.lower() != answer.lower():
            return False
        return super().handle(user, answer)

class Question3Step(Step):
    def handle(self, user, answer):
        if user.security_a3.lower() != answer.lower():
            return False
        return super().handle(user, answer)
