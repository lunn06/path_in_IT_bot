from pydantic import BaseModel
from pydantic_core import from_json

from config import Config

class Answer(BaseModel):
    Answer: str
    RoleTeam: list[int]
    ball: int


class Question(BaseModel):
    Question: str
    Answers: list[Answer]


class BelbinsTest(BaseModel):
    Test: list[Question]


def load_test(config: Config) -> BelbinsTest:
    with open(config.models_path, 'r') as file:
        prepared_questions_json = from_json(file)
    belbins_test = BelbinsTest.model_validate(prepared_questions_json)

    return belbins_test



def _test_path(models_path: str) -> str:
    return
