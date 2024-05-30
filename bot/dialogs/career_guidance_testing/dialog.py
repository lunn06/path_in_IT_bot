import operator

from aiogram.enums import ContentType
from aiogram_dialog import Window, StartMode, Dialog
from aiogram_dialog.widgets.kbd import Multiselect, Button, Back, Row, Start
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from bot import states
from bot.configs import Questions


def get_dialog(questions: Questions):
    windows: list[Window] = []

    questions_with_answers_dict = questions.with_answers
    questions_with_answers = []

    for question_text, answers in questions_with_answers_dict.items():
        question_with_answers = question_text
        question_with_answers += '\n'
        question_with_answers += '\n\n'.join(answers)

    widgets = [
        Const(questions_with_answers[0]),
        # Const(questions[0].question),
        Multiselect(
            Format("✓ {item[0]}"),  # E.g `✓ Apple`
            Format("{item[0]}"),
            id="m_q0",
            # min_selected=1,
            item_id_getter=operator.itemgetter(0),
            items=questions[0].question,
        ),
        Button(Const("Следующий вопрос"), id='b', on_click=on_next_click),
    ]
    if questions[0].image is not None:
        widgets += [
            StaticMedia(
                path=questions[0].image,
                type=ContentType.PHOTO
            ),
        ]
    windows += [Window(
        *widgets,
        state=states.CareerGuidanceTesting.question_1,
        getter=get_data,
    )]
    for i, q in enumerate(questions):
        if i in (0, len(questions) - 1):
            continue
        widgets = [
            Const(questions_with_answers[i]),
            # Const(questions[i].question),
            Multiselect(
                Format("✓ {item[0]}"),  # E.g `✓ Apple`
                Format("{item[0]}"),
                id=f"m_q{i}",
                # min_selected=1,
                item_id_getter=operator.itemgetter(0),
                items=q.question,
            ),
            Row(
                Back(text=Const("Предыдущий вопрос")),
                Button(Const("Следующий вопрос"), id='b', on_click=on_next_click),
            ),
        ]
        if q.image is not None:
            widgets += [
                StaticMedia(
                    path=q.image,
                    type=ContentType.PHOTO
                ),
            ]
        windows += [Window(
            *widgets,
            state=getattr(states.CareerGuidanceTesting, f"question_{i+1}"),
            getter=get_data,
        )]

    widgets = [
        Const(questions_with_answers[-1]),
        Multiselect(
            Format("✓ {item[0]}"),  # E.g `✓ Apple`
            Format("{item[0]}"),
            id=f"m_q{len(questions) - 1}",
            # min_selected=1,
            item_id_getter=operator.itemgetter(0),
            items=questions[-1].question,
        ),
        Row(
            Back(text=Const("Предыдущий вопрос")),
            Button(Const("Закончить тест"), id='b', on_click=on_next_click),
        ),
    ]
    if questions[-1].image is not None:
        widgets += [
            StaticMedia(
                path=questions[-1].image,
                type=ContentType.PHOTO
            ),
        ]
    windows += [
        Window(
            *widgets,
            state=states.CareerGuidanceTesting.question_25,
            getter=get_data,
        ),

    ]

    result = Window(
        Format("{профпригодность}"),
        # *results,
        # Format("\nПодходящая профессия: {профригодность}"),
        # Button(Const("Идём дальше!"), id="next", on_click=menu_start),  # TODO switch to main dialog
        Start(
            Const("Идём дальше!"),
            id="go_main_menu",
            state=states.MenuStates.main,
            mode=StartMode.RESET_STACK
        ),
        state=states.CareerGuidanceTesting.results,
        getter=get_result_data,
    )

    windows += [result]

    return Dialog(
        *windows
    )
