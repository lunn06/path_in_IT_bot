from typing import Type

from aiogram import Router, F
from aiogram_dialog import DialogManager
from aiogram.fsm.state import StatesGroup
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import Message, CallbackQuery
from aiogram_dialog.manager.manager import StartMode

from path_in_IT_bot.database import Database
from path_in_IT_bot.utils import build_main_menu_kb
from path_in_IT_bot.readers.model_reader import TelegramBotModel

router = Router()


@router.message(CommandStart())
async def start_handler(
        msg: Message,
        db: Database,
        menu: Type[StatesGroup],
        dialog_manager: DialogManager
) -> None:
    """
    Функция-обработчик команды /start

    :param DialogManager dialog_manager: объект менеджера диалогов
    :param TelegramBotModel model: объект модели работы бота
    :param Database db: объект базы данных
    :param Message msg: объект сообщения
    """
    start_message: str = "Привет!"
    #await msg.answer(start_message, reply_markup=builder.as_markup())
    await dialog_manager.start(getattr(menu, "greeting"), mode=StartMode.RESET_STACK)


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
