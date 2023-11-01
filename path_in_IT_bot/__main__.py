import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from icecream import install  # type: ignore

install()

from path_in_IT_bot.readers.config_reader import config
from database import Database
from handlers import commands, producers
from path_in_IT_bot.readers.model_reader import TelegramBotModel

dp = Dispatcher(storage=MemoryStorage())


async def main() -> None:
    db: Database = await Database.create()

    with open("models/models.json", 'r') as file:
        model: TelegramBotModel = TelegramBotModel.model_validate_json(file.read())

    bot = Bot(token=config.telegram_bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
    dp.include_router(commands.router)
    dp.include_router(producers.dialog)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot, allowed_updates=dp.resolve_used_update_types(),
        db=db,
        model=model
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
