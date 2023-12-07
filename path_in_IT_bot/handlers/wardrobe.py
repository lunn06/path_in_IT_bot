from string import Template

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from path_in_IT_bot.database import DBUser, connect
from path_in_IT_bot.menu import Menu
from path_in_IT_bot.readers.text_reader import text
from path_in_IT_bot.utils import validated

router = Router()


@router.message(Menu.home)
@router.message(F.text == text.wardrobe_header)
async def garage_incoming_handler(msg: Message, user: DBUser, state: FSMContext) -> None:
    tg_user = validated(msg.from_user)

    async with connect(user) as conn:
        if not await user.is_currency_descripted(tg_user.id, conn=conn):
            user_currency = await user.get_currency(tg_user.id, conn=conn)
            currency_description = Template(text.currency_description).substitute(currency=str(user_currency))
            await msg.answer(currency_description)
            await user.set_currency_descripted(tg_user.id, new_currency_descripted=True, conn=conn)

    await msg.answer(text.wardrobe_greeting)
    await state.set_state(Menu.wardrobe)
