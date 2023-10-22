from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import get_text  # type: ignore

command_router = Router()


@command_router.message(Command("start"))
async def start_handler(msg: Message) -> None:
    """
    Функция-обработчик команды /start

    :param Message msg: объект сообщения
    """
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Пуск!",
        callback_data="launch_message")
    )

    start_message: str | None = await get_text("start_message")
    if start_message is not None:
        await msg.answer(start_message, reply_markup=builder.as_markup())
