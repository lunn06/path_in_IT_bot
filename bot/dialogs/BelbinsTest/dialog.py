from handlers import *
from getters import *


start_window = Window(
    Const(text="Привет, готов пройти тест Белбина?"),
    Row(
        Button(id="1", text=Const("Да!"), on_click=some_handler),
    ),
    state=StartSG.start
)

window_question = Window(
    Format("{text_question_answers}"),
    Format("{current_bank}"),
    Select(
        Format('{item[text]}'),
        id="Select",
        item_id_getter=lambda id: id["id"],
        items="num_answers",
        on_click=answer_handler

    ),
    Button(Const("Далее"), id="1", on_click=chapter_handler),
    getter=question_getter,
    state=StartSG.window_chapter
)

window_answer = Window(
    Format("{text_question_answers}"),
    Select(
        Format('{item}'),
        id="Select",
        item_id_getter=lambda id: id,
        items="balls_row1",
        on_click=write_ball_handler
    ),
    Select(
        Format('{item}'),
        id="Select",
        item_id_getter=lambda id: id,
        items="balls_row2",
        on_click=write_ball_handler
    ),
    getter=answer_getter,
    state=StartSG.window_answer_ball
)

window_conclusion = Window(
    Format("{text}"),
    Select(
        Format('{item[text]}'),
        id="Select",
        item_id_getter=lambda id: id["id"],
        items="indexes",
        on_click=description_role_handler
    ),
    Button(Const("Пройти тест заново"), id="1", on_click=reset_handler),
    getter=conclusion_getter,
    state=StartSG.window_conclusion

)
window_description_role = Window(
    Format("{text_description}"),
    Button(Const("Назад"), id="1", on_click=back_to_conclusion_handler),
    getter=window_description_role_getter,
    state=StartSG.window_description_role
)
start_dialog = Dialog(
    start_window,
    window_question,
    window_answer,
    window_conclusion,
    window_description_role
)


def get_dialog() -> Dialog:
    return start_dialog
