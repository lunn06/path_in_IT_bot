import asyncio
import operator
from enum import StrEnum

from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram_dialog import Window, StartMode, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Multiselect, Button, Back, Row, Start
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from bot import states
from bot.configs import Questions
from bot.configs.questions import QualityNameEnum
from bot.dialogs.career_guidance_test.getters import questions_getter, result_data_getter
from bot.dialogs.career_guidance_test.handlers import on_multiselect_state_changed, on_next_click


def get_start_data() -> dict[str, int]:
    qualities: dict[str, int] = {}

    for e in QualityNameEnum:
        e: type[StrEnum]

        quality_name = str(e.value)
        qualities[quality_name] = 0

    return qualities


async def career_guidance_test_start(message: Message, dialog_manager: DialogManager):
    await message.answer("Добро пожаловать! Перед началом давай пройдем небольшой тест!")
    await asyncio.sleep(1)

    await dialog_manager.start(
        state=states.CareerGuidanceTesting.question_1,
        mode=StartMode.RESET_STACK,
        data={
            "qualities": get_start_data()
        }
    )


def get_dialog(questions: Questions):
    windows: list[Window] = []

    questions_list = questions.questions

    for i, q in enumerate(questions):
        widgets = [
            StaticMedia(
                path=str(q.image_path),
                type=ContentType.PHOTO
            ),
            # Const(questions_with_answers[i]),
            Const(q.with_answers),
            Multiselect(
                Format("✓ {item[0]}"),
                Format("{item[0]}"),
                id=f"question_{i + 1}",
                on_state_changed=on_multiselect_state_changed,
                item_id_getter=operator.itemgetter(0),
                items=q.text,
            ),
            Row(
                Back(
                    text=Const("Предыдущий вопрос"),
                    when="show_previews_button"
                ),
                Button(
                    Const(
                        text="Следующий вопрос" if i != len(questions_list) - 1 else "Закончить тест"
                    ),
                    id='b',
                    on_click=on_next_click,
                ),
            ),
        ]

        windows += [
            Window(
                *widgets,
                state=getattr(states.CareerGuidanceTesting, f"question_{i + 1}"),
                getter=questions_getter,
            )
        ]

    result = Window(
        Format("{career_guidance_test_result}"),
        # *results,
        # Format("\nПодходящая профессия: {профригодность}"),
        # Button(Const("Идём дальше!"), id="next", on_click=menu_start),
        Start(
            Const("Идём дальше!"),
            id="go_main_menu",
            state=states.Menu.main,
            mode=StartMode.RESET_STACK
        ),
        state=states.CareerGuidanceTesting.results,
        getter=result_data_getter,
    )

    windows += [result]

    return Dialog(
        *windows
    )
