import re
import copy
import io

from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.kbd import Row, Button, Select
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Jinja

from LoadData import data
from roles import roles_name, description_roles
from utils import top_max_pairs

from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, InputFile
from aiogram_dialog import Dialog, DialogManager, StartMode, Window


async def answer_getter(**kwargs):
    dialog_manager = kwargs.get("dialog_manager")
    memory_data = dialog_manager.dialog_data
    index_question = memory_data.get("question_index")
    index_answer = memory_data.get("answer_index")
    balls = memory_data.get("bank_of_ball")
    question = data[index_question]["Question"]
    answer = data[index_question]["Answers"][index_answer]["Answer"]
    current_balls = dialog_manager.dialog_data.get("data_balls")
    data_balls = current_balls if current_balls is not None else data
    current_ball = data_balls[index_question]["Answers"][index_answer]["ball"]

    select_ball = "Выберите балл, который вы хотите назначить ответу"
    rows = 2
    border = current_ball + balls
    return {
        "text_question_answers": question + "\n\n" + answer +
                                 "\n\n" + select_ball,
        "balls_row1": [ball for ball in range(border // rows + 1)],
        "balls_row2": [ball for ball in range(border // rows + 1, border + 1)]
    }


async def question_getter(**kwargs):
    dialog_manager: DialogManager = kwargs.get("dialog_manager")
    current_bank = dialog_manager.dialog_data.get("bank_of_ball")
    num_question = dialog_manager.dialog_data.get("question_index")
    print(f"data: {data}")

    len_questions = len(data)
    answers = data[num_question]["Answers"]
    question = data[num_question]["Question"]
    answers_str = "\n\n".join(
        [str(index) + ". " + answer["Answer"] for answer, index in zip(answers, range(1, len(answers) + 1))])
    data_balls = dialog_manager.dialog_data.get("data_balls")
    print(f"balls: {data_balls}")
    balls = data_balls[num_question]["Answers"] if data_balls is not None else answers
    balls = [ball["ball"] for ball in balls]

    return {
        "text_question_answers": f"Вопрос {num_question + 1}/{len_questions} {question}\n\n{answers_str}\n",
        "num_answers": [{"text": f"{num}: {ball} ", "id": f"{num}"} for num, ball in
                        zip(range(1, len(answers) + 1), balls)],
        "current_bank": f"Баллов в банке: {current_bank}. \n\nРаспределите баллы между ответами"
    }


async def conclusion_getter(**kwargs):
    roles = roles_name
    roles_ball = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0
    }

    dialog_manager: DialogManager = kwargs.get("dialog_manager")
    max_bank = dialog_manager.dialog_data.get("max_bank")
    data_balls: dict = dialog_manager.dialog_data.get("data_balls")
    amount_question = len(data_balls)
    for question_index in range(amount_question):
        question: dict = data_balls[question_index]

        for answer_index in range(len(question["Answers"])):
            ball = int(question["Answers"][answer_index]["ball"])
            roles_indexes: [int] = question["Answers"][answer_index]["RoleTeam"]
            print(f"ball: {ball} answer_index: {answer_index}")
            for role in roles_indexes:
                roles_ball[role] += ball / len(roles_indexes)


    max_roles = top_max_pairs(roles_ball, 3)


    some_text = "По итогам пройденного теста ваша роль:\n\n"
    some_text2 = "Хотите пройти тест заново?"
    round_num = 2
    roles_text_info = "\n\n".join(
        [f"{roles_name[role_index]}: {round((max_roles.get(role_index) / (len(data) * max_bank)) * 100, 2)}%" for role_index in
         max_roles.keys()])
    return {
        "text": some_text + roles_text_info,
        "indexes": [{"text": roles_name[role_index], "id": role_index} for role_index in max_roles.keys()],
    }


async def window_description_role_getter(**kwargs):
    dialog_manager: DialogManager = kwargs.get("dialog_manager")
    index_role = dialog_manager.dialog_data.get("index_role")
    return {
        "text_description": f"{roles_name.get(index_role)}\n\n{description_roles.get(index_role)}"
    }
