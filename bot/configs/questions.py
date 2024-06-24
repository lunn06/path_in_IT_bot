from __future__ import annotations

import os
import random
from enum import StrEnum
from functools import lru_cache
from glob import glob
from math import floor
from typing import Any, Optional, override, Iterator

from pydantic import BaseModel, PositiveFloat, FilePath
from pydantic_core import from_json

from bot.configs import parse_config, Config


class Questions(BaseModel):
    questions: list["Question"]

    def __getitem__(self, index: int) -> Question:
        return self.questions[index]

    @override
    def __iter__(self) -> Iterator[Question]:  # type: ignore
        return self.questions.__iter__()


class Question(BaseModel):
    text: str
    image_path: FilePath
    answers: list["Answer"]

    @property
    def with_answers(self) -> str:
        question_with_answers = self.text
        # question_with_answers += '\n\n'.join(answers)

        for i, answer in enumerate(self.answers):
            question_with_answers += f"\n\n{i + 1}. {answer.text}"

        return question_with_answers


class Answer(BaseModel):
    text: str
    qualities: list["Quality"]
    checked: bool


class QualityNameEnum(StrEnum):
    systems_and_mechanisms = "системы и механизмы"
    numbers_and_calculations = "числа и вычисления"
    images_and_visualization = "образы и визуализация"
    people_and_interactions = "люди и взаимодействия"
    texts_and_languages = "тексты и языки"
    organization_and_management = "организация и управление"
    development_and_creation_of_new = "разработка и создание нового"
    research_and_analysis = "исследование и анализ"
    promotion = "продвижение"
    structuring_and_control = "структурирование и контроль"


class Quality(BaseModel):
    name: QualityNameEnum
    points: PositiveFloat
    normalization_coefficient: Optional[PositiveFloat]
    current_points: Optional[PositiveFloat]

    @property
    def normal(self):
        if self.normalization_coefficient is not None:
            return self.current_points * self.normalization_coefficient
        raise ValueError(f"Quality: {self.name} is not has normalization coefficient")


@lru_cache(maxsize=1)
def parse_questions(config: Config) -> Questions:
    prepared_questions_json = _prepare_json(str(config.models_path))
    # pprint(prepared_questions_json)
    questions = Questions.model_validate(prepared_questions_json)
    _normalize_points(questions)

    return questions


def _normalize_points(questions: Questions):
    max_values: dict[str, float] = {}

    for question in questions.questions:
        for answer in question.answers:
            for quality in answer.qualities:
                if quality.name in max_values.keys():
                    max_values[quality.name] += quality.points
                else:
                    max_values[quality.name] = quality.points

    max_value = max(max_values.values())
    for question in questions.questions:
        for answer in question.answers:
            for quality in answer.qualities:
                sum_points = max_values[quality.name]
                quality.normalization_coefficient = floor(max_value / sum_points)


def _question_path(models_path: str) -> str:
    return f"{models_path}{os.sep}questions.json"


def _images_path(models_path: str) -> str:
    return f"{models_path}{os.sep}images{os.sep}"


def _random_image_path(question_images_path: str, question_number) -> Optional[str]:
    question_images_path = f"{question_images_path}Вопрос {question_number}{os.sep}"
    question_images = [image for image in glob(question_images_path + "*")]
    if len(question_images) > 0:
        return random.choice(question_images)
    else:
        return None


@lru_cache(maxsize=1)
def _prepare_json(models_path: str) -> dict[Any, Any]:
    questions_path = _question_path(models_path)
    images_path = _images_path(models_path)
    with open(questions_path, 'r') as questions_file:
        questions_json: dict[Any, Any] = from_json(questions_file.read(), cache_strings=True)

    prepared_json: dict[str, Any] = {"questions": []}
    for question_i, t in enumerate(questions_json.items()):
        question, answers_dict = t
        question_number = question_i + 1
        image_path = _random_image_path(images_path, question_number)
        question_dict = {
            "text": question,
            "image_path": image_path,
            "answers": []
        }
        for answer, qualities_dict in answers_dict.items():
            answer_dict = {
                "text": answer,
                "qualities": [],
                "checked": False
            }
            for quality, points in qualities_dict.items():
                answer_dict["qualities"] += [{
                    "name": quality.lower(),
                    "points": points,
                    "normalization_coefficient": None,
                    "current_points": None
                }]
            question_dict["answers"] += [answer_dict]

        prepared_json["questions"] += [question_dict]

    return prepared_json


if __name__ == '__main__':
    config = parse_config()
    questions: Questions = parse_questions(config)
    # assert parse_questions(config) is parse_questions(config)
    assert parse_config() is parse_config()
