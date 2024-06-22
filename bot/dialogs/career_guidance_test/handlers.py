from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedMultiselect, Next

from bot.configs import Question


async def on_multiselect_state_changed(
        _callback: CallbackQuery,
        _widget: ManagedMultiselect,
        manager: DialogManager,
        clicked_item: str
):
    # print(widget.get_checked(), clicked_item, manager.current_context().state.state)
    questions = manager.middleware_data["questions"]
    state_name = manager.current_context().state.state
    question_num = extract_question_number(state_name)

    selected_answers = manager.dialog_data.get(state_name, [])
    current_points = manager.start_data["qualities"]
    current_question: Question = questions[question_num - 1]

    answer_qualities = current_question.answers[int(clicked_item) - 1].qualities
    decrease = clicked_item in selected_answers

    if decrease:
        selected_answers.remove(clicked_item)
    else:
        selected_answers.append(clicked_item)

    for quality in answer_qualities:
        if decrease:
            current_points[quality.name] = current_points[quality.name] - quality.points
        else:
            current_points[quality.name] = current_points[quality.name] + quality.points

    manager.dialog_data[state_name] = selected_answers


async def on_next_click(
        callback: CallbackQuery,
        # multiselect: ManagedMultiselect,
        _button: Next,
        manager: DialogManager
):
    current_context = manager.current_context()
    state_name = current_context.state.state

    for question_id, answers in current_context.widget_data.items():
        if state_name.endswith(question_id):
            if len(answers) == 0:
                await callback.answer("Нужно выбрать хотя бы один вариант ответа!")
            else:
                await manager.next()
            break

def extract_question_number(question_state: str) -> int:
    return int(question_state.split('_')[-1])
