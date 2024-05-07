from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup

from bot.database import DBUser
from bot.menu import Menu
from bot.readers.text_reader import text
from bot.utils import build_inline_start_kb, validated
from bot.utils import build_kb

router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message, user: DBUser, state: FSMContext) -> None:
    """
    Функция-обработчик команды /start

    :param state:
    :param User user: объект базы данных
    :param Message msg: объект сообщения
    """
    tg_user = validated(msg.from_user)

    await user.add(tg_user.id)
    # record_list = await user.get(user.id)
    # for record in record_list:
    #     await msg.answer(" ".join(map(str, record)))

    start_message: str = text.start_message
    keyboard = build_inline_start_kb(callback_data="launch_message")
    await msg.answer(start_message, reply_markup=keyboard)
    await state.set_state(default_state)


@router.callback_query(F.data == "launch_message")
async def send_launch_message(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Функция-колбек, вызываемая при возврате в главное меню
    Её главная задача - отображать клавиатуру с ключевыми пунктами меню

    :param state:
    :param TelegramBotModel model: объект модели работы бота
    :param CallbackQuery callback: объект колбека для
    """

    kb = build_kb((
        text.test_header,
        text.garage_header,
        text.kitchen_header,
        text.wardrobe_header,
        text.interview_header,
    ))
    keyboard = ReplyKeyboardMarkup(keyboard=kb)

    launch_message = text.launch_message
    await validated(callback.message).answer(launch_message, reply_markup=keyboard)
    await state.set_state(Menu.home)
