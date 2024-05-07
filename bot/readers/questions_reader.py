import json
import os
import random
from glob import glob

from bot.entities.question import Question
from bot.readers.config_reader import config

questions_list: list[Question] = []

questions_path = str(config.models_path) + os.sep + "questions.json"
images_path = str(config.models_path) + os.sep + "images"
image_path_template = "Вопрос {}"
with open(questions_path, 'r') as file:
    questions = json.loads(file.read())
    for i, q in enumerate(questions.keys()):
        image_dir_path = images_path + os.sep + image_path_template.format(i+1)
        try:
            images = [image for image in glob(image_dir_path + os.sep + "*.png")]
            image = random.choice(images)
        except IndexError:
            image = None
        finally:
            questions_list += [Question(q, questions[q], image)]
