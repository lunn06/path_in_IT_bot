import re
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bot.configs import BelbinsTest
from bot.states import StartSG


async def some_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(question_index=0, bank_of_ball=10, max_bank=10)
    await dialog_manager.next()


async def reset_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(question_index=0, bank_of_ball=10, data_balls=None, answer_index=0, index_role=-1)
    await dialog_manager.switch_to(StartSG.window_chapter)


async def back_to_conclusion_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(StartSG.window_conclusion)


async def description_role_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, *args,
                                   **kwargs):
    match = re.search(r'\d+$', callback.data)
    if match:
        index_role = match.group()
        dialog_manager.dialog_data.update(index_role=int(index_role))
        await dialog_manager.switch_to(StartSG.window_description_role)


async def chapter_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    current_bank = dialog_manager.dialog_data.get("bank_of_ball")
    if current_bank > 0:
        await callback.answer("Для перехода к следующему вопросу, банк баллов должен быть пустым.", show_alert=True)
        return

    all_questions = len(dialog_manager.middleware_data["belbins_test"].Test)
    current_question = dialog_manager.dialog_data.get("question_index") + 1
    if all_questions > current_question:
        dialog_manager.dialog_data.update(question_index=dialog_manager.dialog_data.get("question_index") + 1,
                                          bank_of_ball=10)
        await dialog_manager.switch_to(StartSG.window_chapter)
    else:
        await dialog_manager.switch_to(StartSG.window_conclusion)


async def answer_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, *args, **kwargs):
    match = re.search(r'\d+$', callback.data)
    if match:
        index_answer = match.group()
        dialog_manager.dialog_data.update(answer_index=int(index_answer) - 1)
        await dialog_manager.switch_to(StartSG.window_answer_ball)


async def write_ball_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, *args, **kwargs):
    match = re.search(r'\d+$', callback.data)
    memory_data = dialog_manager.dialog_data
    if match:
        current_ball = int(match.group())

        question_index = memory_data.get("question_index")
        answer_index = memory_data.get("answer_index")
        bank = memory_data.get("bank_of_ball")

        data_balls = {}
        if memory_data.get("data_balls") is not None:
            data_balls = memory_data.get("data_balls")
        else:
            data_balls: BelbinsTest = list(dialog_manager.middleware_data["belbins_test"])

        old_ball = data_balls.Test[question_index].Answers[answer_index].ball
        new_bank = bank - current_ball + old_ball
        data_balls.Test[question_index].Answers[answer_index].ball = current_ball
        dialog_manager.dialog_data.update(data_balls=data_balls)

        dialog_manager.dialog_data.update(bank_of_ball=new_bank)

        await dialog_manager.switch_to(StartSG.window_chapter)

# @dp.message(CommandStart())
# async def command_start_process(message: Message, dialog_manager: DialogManager):
#     await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)