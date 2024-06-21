from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from bot.states import Recommendations


def get_dialog() -> Dialog:
    recommendations_dialog = Dialog(
        Window(
            Const("Модуль не готов"),
            Cancel(Const("Назад")),
            state=Recommendations.unimplemented
        )
    )

    return recommendations_dialog
