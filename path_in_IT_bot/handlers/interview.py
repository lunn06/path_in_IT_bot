from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram_dialog import setup_dialogs, StartMode, DialogManager  # noqa: F401

from path_in_IT_bot.database import DBUser
from path_in_IT_bot.factories.dialog_factory import DialogFactory
from path_in_IT_bot.menu import Menu
from path_in_IT_bot.templates import dialog_handler_env
from path_in_IT_bot.utils import validated, build_kb, random_str

router = Router()
factory = DialogFactory("/home/dcdnc/mycod/python/path_in_IT_bot/models/interviews")

for item in factory.items:
    router.include_router(item.dialog)

setup_dialogs(router)

t = dialog_handler_env
for item in factory.items:
    render = t.render(
        item=item,
        handler_id=random_str(5),
    )
    exec(render)


@router.message(F.text == "Собеседование")
async def garage_incoming_handler(msg: Message, user: DBUser, state: FSMContext) -> None:
    tg_user = validated(msg.from_user)

    kb = build_kb([dialog.name for dialog in factory.items])
    keyboard = ReplyKeyboardMarkup(keyboard=kb)

    interview_greeting = "Интервью"
    await msg.answer(interview_greeting, reply_markup=keyboard)
    await state.set_state(Menu.interview)
