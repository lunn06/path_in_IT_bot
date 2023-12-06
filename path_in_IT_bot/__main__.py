import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from path_in_IT_bot.database import DBUser
from path_in_IT_bot.handlers import commands
# from path_in_IT_bot.readers.model_reader import model
from path_in_IT_bot.handlers import garage, kitchen, wardrobe, interview
from path_in_IT_bot.readers.config_reader import config

# from path_in_IT_bot.factories.producers_factory import ProducersFactory
# from path_in_IT_bot.builders.dialogs_builder import DialogsBuilder
# from path_in_IT_bot.builders.states_builder import StatesGroupBuilder


# redis_client = Redis()
# dp = Dispatcher(storage=RedisStorage(redis_client))
dp = Dispatcher(storage=MemoryStorage())


async def main() -> None:
    db: DBUser = await DBUser.create()

    bot = Bot(token=config.telegram_bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
    dp.include_router(commands.router)
    dp.include_router(garage.router)
    dp.include_router(kitchen.router)
    dp.include_router(wardrobe.router)
    dp.include_router(interview.router)

    # menu_builder = StatesGroupBuilder(*model.producers.keys())
    # menu_builder.add("greeting")
    #
    # menu = menu_builder.build()
    #
    # producers_factory = ProducersFactory()
    # for producer in producers_factory.items:
    #     dialog = DialogsBuilder.build_from(producer, menu)
    #     dp.include_router(dialog)
    #
    # setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        user=db,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
