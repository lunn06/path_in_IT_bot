from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from path_in_IT_bot.database import Database
from path_in_IT_bot.readers.model_reader import TelegramBotModel
from path_in_IT_bot.utils import build_main_menu_kb

router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message, db: Database, model: TelegramBotModel) -> None:
    """
    Функция-обработчик команды /start

    :param TelegramBotModel model: объект модели работы бота
    :param Database db: объект базы данных
    :param Message msg: объект сообщения
    """
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Пуск!",
        callback_data="launch_message")
    )

    if msg.from_user is not None:
        await db.add_new_user(msg.from_user.id)

    start_message: str | None = "Привет!"
    if start_message is not None:
        await msg.answer(start_message, reply_markup=builder.as_markup())


@router.callback_query(F.data == "launch_message")
async def send_launch_message(callback: CallbackQuery, model: TelegramBotModel) -> None:
    """
    Функция-колбек, вызываемая при возврате в главное меню
    Её главная задача - отображать клавиатуру с ключевыми пунктами меню

    :param TelegramBotModel model: объект модели работы бота
    :param CallbackQuery callback: объект колбека для
    """

    kb = build_main_menu_kb()

    keyboard = ReplyKeyboardMarkup(keyboard=kb)

    launch_message = "Пуск!"
    if isinstance(launch_message, str):
        await callback.message.answer(launch_message, reply_markup=keyboard)  # type: ignore
