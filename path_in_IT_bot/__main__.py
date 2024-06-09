import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from bot.configs import Config, parse_config, Questions, parse_questions
from path_in_IT_bot.handlers import professional_test
# from path_in_IT_bot.readers.config_reader import config

# redis_client = Redis()
# dp = Dispatcher(storage=RedisStorage(redis_client))
dp = Dispatcher(storage=MemoryStorage())


async def main() -> None:
    # db: DBUser = await DBUser.create()

    config: Config = parse_config()
    questions: Questions = parse_questions(config)

    bot = Bot(token=config.telegram_bot_token.get_secret_value(), parse_mode=ParseMode.MARKDOWN)

    # dp.include_router(interview.router)
    # dp.include_router(commands.router)
    dp.include_router(professional_test.proftest_dialog)
    dp.include_router(professional_test.menu_dialog)
    dp.include_router(professional_test.practice_dialog)
    dp.include_router(professional_test.recommendations_dialog)
    # dp.include_router(garage.router)
    # dp.include_router(kitchen.router)
    # dp.include_router(wardrobe.router)
    # dp.include_router(interview.router)

    dp.message.register(professional_test.proftest_first_start)

    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        questions=questions
        # user=db,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
