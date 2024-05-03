import asyncio
import logging

import aiogram_dialog.widgets.text
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from path_in_IT_bot.database import DBUser
from path_in_IT_bot.handlers import commands, garage, kitchen, wardrobe, interview, professional_test
from path_in_IT_bot.readers.config_reader import config

# redis_client = Redis()
# dp = Dispatcher(storage=RedisStorage(redis_client))
dp = Dispatcher(storage=MemoryStorage())


async def main() -> None:
    # db: DBUser = await DBUser.create()

    bot = Bot(token=config.telegram_bot_token.get_secret_value(), parse_mode=ParseMode.HTML)

    # dp.include_router(interview.router)
    # dp.include_router(commands.router)
    dp.include_router(professional_test.router)
    # dp.include_router(garage.router)
    # dp.include_router(kitchen.router)
    # dp.include_router(wardrobe.router)
    # dp.include_router(interview.router)

    dp.message.register(professional_test.start)

    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        # user=db,
    )

    aiogram_dialog.widgets.text.List

    # dp.run_polling()

    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
