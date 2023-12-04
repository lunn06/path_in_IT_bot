from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup

from path_in_IT_bot.database import DBUser
from path_in_IT_bot.utils import build_kb
from path_in_IT_bot.utils import get_text, build_inline_start_kb, validated

router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message, user: DBUser, state: FSMContext) -> None:
    """
    Функция-обработчик команды /start

    :param User user: объект базы данных
    :param Message msg: объект сообщения
    """
    tg_user = validated(msg.from_user)

    await user.add(tg_user.id)
    # record_list = await user.get(user.id)
    # for record in record_list:
    #     await msg.answer(" ".join(map(str, record)))

    start_message: str = await get_text("start_message", name=tg_user.first_name)
    keyboard = await build_inline_start_kb(callback_data="launch_message")
    await msg.answer(start_message, reply_markup=keyboard)
    await state.set_state(default_state)


@router.callback_query(F.data == "launch_message")
async def send_launch_message(callback: CallbackQuery) -> None:
    """
    Функция-колбек, вызываемая при возврате в главное меню
    Её главная задача - отображать клавиатуру с ключевыми пунктами меню

    :param TelegramBotModel model: объект модели работы бота
    :param CallbackQuery callback: объект колбека для
    """

    kb = build_kb((
        "Гараж", "Кухня", "Гардероб", "Собеседование"
    ))
    keyboard = ReplyKeyboardMarkup(keyboard=kb)

    launch_message = await get_text("launch_message")
    await validated(callback.message).answer(launch_message, reply_markup=keyboard)
