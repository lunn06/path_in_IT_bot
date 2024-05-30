from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Start, Group, Keyboard
from aiogram_dialog.widgets.text import Const

from path_in_IT_bot.factories.dialogs_factory import DialogsFactory
from path_in_IT_bot.menu import Menu
from path_in_IT_bot.readers.config_reader import config
from path_in_IT_bot.readers.text_reader import text


class MainInterview(StatesGroup):
    menu = State()


interview_path = str(config.models_path.joinpath("interviews"))
factory = DialogsFactory(interview_path)

router = Router()

group_widgets: list[Keyboard] = []
for item in factory.items:
    group_widgets += [Start(
        Const(item.name),
        id=item.name.lower().replace(" ", "_"),
        data=item,
        state=getattr(item._states, f"state_{item.root.id}")
    )]

    router.include_router(item.dialog)

group = Group(*group_widgets, width=config.interview_column_wight)

main_interview_menu_window = Window(
    Const(text.interview_greeting),
    group,
    state=MainInterview.menu
)

main_interview_menu_dialog = Dialog(main_interview_menu_window)
router.include_router(main_interview_menu_dialog)


@router.message(Menu.home)
@router.message(F.text == text.interview_header)
async def start_interview_dialog(_message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        MainInterview.menu,
        # data=factory.items[0],
        mode=StartMode.RESET_STACK,
    )
