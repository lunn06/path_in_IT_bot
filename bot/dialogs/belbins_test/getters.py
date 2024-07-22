from bot.configs import BelbinsTest
from bot.configs.belbins_test_questions import Question, Answer
from roles import roles_name, description_roles
from bot.utils import top_max_pairs

from aiogram_dialog import DialogManager


async def answer_getter(belbins_test: BelbinsTest, dialog_manager: DialogManager):
    #dialog_manager = kwargs.get("dialog_manager")
    memory_data = dialog_manager.dialog_data
    index_question = memory_data.get("question_index")
    index_answer = memory_data.get("answer_index")
    balls = memory_data.get("bank_of_ball")
    question: str = belbins_test.Test[index_question].Question
    answer: str = belbins_test.Test[index_question].Answers[index_answer].Answer
    current_balls: list[Question] = dialog_manager.dialog_data.get("data_balls").Test
    data_balls: list[Question] = current_balls if current_balls is not None else belbins_test.Test
    current_ball: int = data_balls[index_question].Answers[index_answer].ball

    select_ball = "Выберите балл, который вы хотите назначить ответу"
    rows = 2
    border = current_ball + balls
    return {
        "text_question_answers": question + "\n\n" + answer +
                                 "\n\n" + select_ball,
        "balls_row1": [ball for ball in range(border // rows + 1)],
        "balls_row2": [ball for ball in range(border // rows + 1, border + 1)]
    }


async def question_getter(belbins_test: BelbinsTest, dialog_manager: DialogManager):
    #dialog_manager: DialogManager = kwargs.get("dialog_manager")
    current_bank = dialog_manager.dialog_data.get("bank_of_ball")
    num_question = dialog_manager.dialog_data.get("question_index")

    questions: list[Question] = belbins_test.Test
    len_questions = len(questions)
    question: str = questions[num_question].Question
    answers: list[Answer] = questions[num_question].answers
    #answers = data[num_question]["Answers"]
    #question = data[num_question]["Question"]
    answers_str = "\n\n".join(
        [str(index) + ". " + answer.Answer for answer, index in zip(answers, range(1, len(answers) + 1))])
    data_balls: list[Question] = dialog_manager.dialog_data.get("data_balls").Test
    balls: list[Answer] = data_balls[num_question].Answers if data_balls is not None else answers
    balls = [ball.Answer for ball in balls]

    return {
        "text_question_answers": f"Вопрос {num_question + 1}/{len_questions} {question}\n\n{answers_str}\n",
        "num_answers": [{"text": f"{num}: {ball} ", "id": f"{num}"} for num, ball in
                        zip(range(1, len(answers) + 1), balls)],
        "current_bank": f"Баллов в банке: {current_bank}. \n\nРаспределите баллы между ответами"
    }


async def conclusion_getter(belbins_test: BelbinsTest, dialog_manager: DialogManager):
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

    #dialog_manager: DialogManager = kwargs.get("dialog_manager")
    max_bank = dialog_manager.dialog_data.get("max_bank")
    data_balls: list[Question] = dialog_manager.dialog_data.get("data_balls").Test
    amount_question = len(data_balls)
    for question_index in range(amount_question):
        question: Question = data_balls[question_index]

        for answer_index in range(len(question.Answers)):
            ball = int(question.Answers[answer_index].ball)
            roles_indexes: [int] = question.Answers[answer_index].RoleTeam
            print(f"ball: {ball} answer_index: {answer_index}")
            for role in roles_indexes:
                roles_ball[role] += ball / len(roles_indexes)

    max_roles = top_max_pairs(roles_ball, 3)

    some_text = "По итогам пройденного теста ваша роль:\n\n"
    some_text2 = "Хотите пройти тест заново?"
    round_num = 2
    roles_text_info = "\n\n".join(
        [f"{roles_name[role_index]}: {round((max_roles.get(role_index) / (len(data_balls) * max_bank)) * 100, 2)}%" for
         role_index in
         max_roles.keys()])
    return {
        "text": some_text + roles_text_info,
        "indexes": [{"text": roles_name[role_index], "id": role_index} for role_index in max_roles.keys()],
    }


async def window_description_role_getter(dialog_manager: DialogManager):
    index_role = dialog_manager.dialog_data.get("index_role")
    return {
        "text_description": f"{roles_name.get(index_role)}\n\n{description_roles.get(index_role)}"
    }
