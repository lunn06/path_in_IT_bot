class Question:
    def __init__(self, question: str, answers: dict[str, dict[str, float | int]]):
        self.question = question
        self.answers = answers
