from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram_dialog import setup_dialogs, StartMode, DialogManager  # noqa: F401
from jinja2.nativetypes import NativeEnvironment

from path_in_IT_bot.menu import Menu
from path_in_IT_bot.database import DBUser
from path_in_IT_bot.factories.dialog_factory import DialogFactory
from path_in_IT_bot.utils import validated, build_kb, random_str

router = Router()
factory = DialogFactory("/home/dcdnc/mycod/python/path_in_IT_bot/models/interviews")

for item in factory.items:
    router.include_router(item.dialog)

    # @router.message(Menu.interview)
    # @router.message(F.text == dialog.name)
    # async def dialog_handler(
    #         msg: Message,
    #         user: DBUser,
    #         dialog_manager: DialogManager
    # ) -> None:
    #     for sub_dialog in factory.items:
    #         if sub_dialog.name == dialog.name:
    #             await dialog_manager.start(
    #                 getattr(dialog.states, f"state_{dialog.root.id}"),
    #                 mode=StartMode.RESET_STACK
    #             )
    #             break

setup_dialogs(router)

dialog_handler_template = '''
@router.message(Menu.interview)
@router.message(F.text == "{{ item.name }}")
async def dialog_{{ handler_id }}_handler(
    msg: Message, 
    user: DBUser, 
    dialog_manager: DialogManager
) -> None:
    for item in factory.items:
        if item.name == "{{ item.name }}":
            await dialog_manager.start(
                getattr(item.states, "state_{{ item.root.id }}"),
                data=item,
                mode=StartMode.NEW_STACK
            )
            break
'''

env = NativeEnvironment()
t = env.from_string(dialog_handler_template)
# render = t.render(
#     dialogs=factory.items,
#     dialog_id=random_str(5),
# )
# print(render)
# exec(render)


for item in factory.items:
    render = t.render(
        item=item,
        handler_id=random_str(5),
    )
    print(item.name)
    exec(render)


@router.message(F.text == "Собеседование")
async def garage_incoming_handler(msg: Message, user: DBUser, state: FSMContext) -> None:
    tg_user = validated(msg.from_user)

    kb = build_kb([dialog.name for dialog in factory.items])
    keyboard = ReplyKeyboardMarkup(keyboard=kb)

    interview_greeting = "Интервью"
    await msg.answer(interview_greeting, reply_markup=keyboard)
    await state.set_state(Menu.interview)
