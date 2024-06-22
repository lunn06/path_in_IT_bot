import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from fluentogram import TranslatorHub
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.configs import Config, Questions, parse_config, parse_questions
from bot.core.classification import ProfModel
from bot.database.base import Base
from bot.database.requests import test_connection
from bot.middlewares import DatabaseSessionMiddleware, TranslatorRunnerMiddleware
from bot.utils.i18n import create_translator_hub
from bot.dialogs import career_guidance_test, menu, recomendations, practice, greeting


async def main() -> None:
    config: Config = parse_config()
    questions: Questions = parse_questions(config)

    translator_hub: TranslatorHub = create_translator_hub()

    prof_model = ProfModel.default()

    # engine = create_async_engine(url=str(config.db_url), echo=True)
    #
    # meta = Base.metadata
    # async with engine.begin() as conn:
    #     if config.debug_mode:
    #         await conn.run_sync(meta.drop_all)
    #     await conn.run_sync(meta.create_all)

    # session_maker = async_sessionmaker(engine, expire_on_commit=config.debug_mode)

    # async with session_maker() as session:
    #     await test_connection(session)

    bot = Bot(
        token=config.telegram_bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(menu.get_dialog())
    dp.include_router(career_guidance_test.get_dialog(questions))
    dp.include_router(recomendations.get_dialog())
    dp.include_router(practice.get_dialog())

    dp.message.register(career_guidance_test.career_guidance_test_start)

    # dp.update.middleware(DatabaseSessionMiddleware(session_pool=session_maker))
    dp.update.middleware(TranslatorRunnerMiddleware())

    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        questions=questions,
        prof_model=prof_model,
        _translator_hub=translator_hub
        # user=db,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
