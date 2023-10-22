from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import get_text  # type: ignore
from states import Menu  # type: ignore

garage_router = Router()


@garage_router.message(F.text == "Гараж")
async def becoming_in_garage_handler(msg: Message, state: FSMContext):
    garage_greeting: str | None = await get_text("garage_greeting")
    if garage_greeting is not None:
        await msg.answer(garage_greeting)
    await state.set_state(Menu.garage)
