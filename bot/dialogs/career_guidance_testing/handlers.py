from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedMultiselect
from aiogram_dialog.widgets.kbd import Button


async def on_next_click(
        message: CallbackQuery,
        multiselect: ManagedMultiselect,
        manager: DialogManager
):

    multiselect.get_checked()


    widget_id = 'm_' + manager.current_context().state.state[-3:].removeprefix('_')
    question_id = int(widget_id.removeprefix('m_q'))
    data = manager.current_context().widget_data

    for j, a in enumerate(questions[question_id].answers.keys()):
        if str(j) not in data[widget_id]:
            continue
        for cr, points in questions[question_id].answers[a].items():
            print(cr, points)
            if cr.lower() in manager.dialog_data.keys():
                manager.dialog_data[cr.lower()] += points
            else:
                manager.dialog_data[cr.lower()] = points
    print(data, widget_id, manager.dialog_data)

    if len(data[widget_id]) < 1:
        await message.answer("Нужно выбрать хотя бы один вариант ответа!")
    else:
        await manager.next()
