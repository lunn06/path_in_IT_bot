from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from bot.states import Practice


def get_dialog() -> Dialog:
    practice_dialog = Dialog(
        Window(
            Const("Модуль не готов"),
            Cancel(Const("Назад")),
            state=Practice.unimplemented
        )
    )

    return practice_dialog
