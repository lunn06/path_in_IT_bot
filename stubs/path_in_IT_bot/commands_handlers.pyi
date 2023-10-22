from _typeshed import Incomplete
from aiogram.types import Message as Message

command_router: Incomplete

async def start_handler(msg: Message) -> None:
    """
    Функция-обработчик команды /start

    :param Message msg: объект сообщения
    """
