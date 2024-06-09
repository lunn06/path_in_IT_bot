class Question:
    def __init__(self, question: str, answers: dict[str, dict[str, float | int]], image: str = None):
        self.question = question
        self.answers = answers
        self.image = image
