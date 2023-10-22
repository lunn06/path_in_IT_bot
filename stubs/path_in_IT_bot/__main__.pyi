from _typeshed import Incomplete
from aiogram.types.callback_query import CallbackQuery as CallbackQuery

dp: Incomplete

async def main() -> None: ...
async def send_launch_message(callback: CallbackQuery) -> None:
    """
    Функция-колбек, вызываемая при возврате в главное меню
    Её главная задача - отображать клавиатуру с ключевыми пунктами меню

    :param CallbackQuery callback: объект колбека для
    """
