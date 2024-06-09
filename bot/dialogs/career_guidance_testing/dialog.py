from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, Cancel
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from .states import MenuStates, GreetingStates, Recommendations, Practice
from . import states
def max_values(iterable):
    max_val = iterable[0]
    for item in iterable:
        if item > max_val:
            max_val = item
    return max_val
recommendations_dialog = Dialog(
    Window(
        Const("Модуль не готов"),
        Cancel(Const("Назад")),
        state=Recommendations.unimplemented
    )
)

practice_dialog = Dialog(
    Window(
        Const("Модуль не готов"),
        Cancel(Const("Назад")),
        state=Practice.unimplemented
    )
)

menu_dialog = Dialog(
    Window(
        Const("Добро пожаловать в главное меню!"),
        Start(
            Const("Тест на профориентацию"),
            id="123",
            state=states.state_q0,
            data=max_values,
        ),
        Start(
            Const("Рекомендации"),
            id="1",
            state=Recommendations.unimplemented,
        ),
        Start(
            Const("Практикум"),
            id="2",
            state=Practice.unimplemented,
        ),
        markup_factory=ReplyKeyboardFactory(resize_keyboard=True, one_time_keyboard=True),
        state=MenuStates.main,
    )
)

greeting_dialog = Dialog(
    Window(
        Const("Привет! Перед тем как начать, я предлагаю тебе пройти небольшой тест!"),
        Start(
            Const("Начать тест"),
            id="123",
            state=states.state_q0,
            data=max_values,
        ),
        state=GreetingStates.main
    ),
)