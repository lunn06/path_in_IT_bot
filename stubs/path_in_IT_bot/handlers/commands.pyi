from _typeshed import Incomplete
from aiogram.filters import Command as Command
from aiogram.types import CallbackQuery as CallbackQuery, KeyboardButton as KeyboardButton, Message as Message
from path_in_IT_bot.database import Database as Database
from path_in_IT_bot.readers.model_reader import TelegramBotModel as TelegramBotModel
from path_in_IT_bot.utils import build_main_menu_kb as build_main_menu_kb

router: Incomplete

async def start_handler(msg: Message, db: Database, model: TelegramBotModel) -> None: ...
async def send_launch_message(callback: CallbackQuery, model: TelegramBotModel) -> None: ...
