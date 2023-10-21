import os
import asyncio
import logging

import aiogram.types as types
from aiogram import Bot, Dispatcher, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types.callback_query import CallbackQuery

from dotenv import load_dotenv

from utils import get_text
from commands_handlers import command_router
from garage_handlers import garage_router

load_dotenv()

dp = Dispatcher(storage=MemoryStorage())


async def main() -> None:
    telegram_bot_token: str | None = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = Bot(token=telegram_bot_token, parse_mode=ParseMode.HTML)  # type: ignore
    dp.include_router(command_router)
    dp.include_router(garage_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


@dp.callback_query(F.data == "launch_message")
async def send_launch_message(callback: CallbackQuery) -> None:
    """
    Функция-колбек, вызываемая при возврате в главное меню
    Её главная задача - отображать клавиатуру с ключевыми пунктами меню

    :param CallbackQuery callback: объект колбека для
    """

    kb = [
        [types.KeyboardButton(text="Гараж")],
        [types.KeyboardButton(text="Кухня")],
        [types.KeyboardButton(text="Гардероб")],
        [types.KeyboardButton(text="Пойти на собеседование просто так")],
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)

    launch_message: str | None = await get_text("launch_message")
    if launch_message is not None:
        await callback.message.answer(launch_message, reply_markup=keyboard) # type: ignore


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
