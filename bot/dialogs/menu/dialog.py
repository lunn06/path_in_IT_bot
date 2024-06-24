from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Const

from bot import states
from bot.dialogs import career_guidance_test


def get_dialog() -> Dialog:
    windows: list[Window] = []

    menu_window = Window(
        Const("Добро пожаловать в главное меню!"),
        # TextInput(
        #     id="proftest",
        #     type_factory=message_approve("Тест на профориентацию"),
        #     on_success=proftest_start,
        #     on_error=unexpected_message,
        # ),
        Start(
            Const("Тест на профориентацию"),
            id="123",
            state=states.CareerGuidanceTesting.question_1,
            # on_click=proftest_from_button_start,
            data={
                "qualities": career_guidance_test.dialog.get_start_data()
            },
        ),
        Start(
            Const("Рекомендации"),
            id="1",
            state=states.Recommendations.unimplemented,
        ),
        Start(
            Const("Практикум"),
            id="2",
            state=states.Practice.unimplemented,
        ),
        markup_factory=ReplyKeyboardFactory(resize_keyboard=True, one_time_keyboard=True),
        state=states.Menu.main,
    )

    windows += [menu_window]

    menu_dialog = Dialog(*windows)

    return menu_dialog
