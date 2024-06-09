from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from . import states
from dialog import Start
from .models import model
from .question import questions, questions_with_answers
from aiogram.utils.formatting import Italic, Bold
def max_values(iterable):
    max_val = iterable[0]
    for item in iterable:
        if item > max_val:
            max_val = item
    return max_val

async def proftest_first_start(message: Message, dialog_manager: DialogManager):
    await message.answer("Добро пожаловать! Перед началом давай пройдем небольшой тест!")
    await dialog_manager.start(state=states.state_q0, mode=StartMode.RESET_STACK, data=max_values)

async def proftest_from_button_start(callback: CallbackQuery, button: Start, manager: DialogManager):
    await manager.start(state=button.state, data=button.start_data, show_mode=button.mode)

async def on_next_click(
        message: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    widget_id = 'm_' + manager.current_context().state.state[-3:].removeprefix('_')
    question_id = int(widget_id.removeprefix('m_q'))
    data = manager.current_context().widget_data

    for j, a in enumerate(questions[question_id].answers.keys()):
        if str(j) not in data[widget_id]:
            continue
        for cr, points in questions[question_id].answers[a].items():
            if cr.lower() in manager.dialog_data.keys():
                manager.dialog_data[cr.lower()] += points
            else:
                manager.dialog_data[cr.lower()] = points

    if len(data[widget_id]) < 1:
        await message.answer("Нужно выбрать хотя бы один вариант ответа!")
    else:
        await manager.next()

    for k, v in manager.current_context().widget_data.items():
        if k.startswith('m_q') and len(v) < 1:
            break

async def get_data(**_kwargs):
    return {
        q.question: tuple((str(i + 1), list(q.answers.keys())[i]) for i in range(len(q.answers.keys()))) for q in questions
    }
