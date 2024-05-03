import json
import os

from path_in_IT_bot.entities.question import Question
from path_in_IT_bot.readers.config_reader import config

questions_list: list[Question] = []

questions_path = str(config.models_path) + os.sep + "questions.json"
with open(questions_path, 'r') as file:
    questions = json.loads(file.read())
    for q in questions.keys():
        questions_list += [Question(q, questions[q])]
