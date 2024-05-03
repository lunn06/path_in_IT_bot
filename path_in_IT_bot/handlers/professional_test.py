import operator

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Multiselect, Back, Button
from aiogram_dialog.widgets.text import Format, Const

from path_in_IT_bot.builders.states_group_builder import StatesGroupBuilder
from path_in_IT_bot.classificator import ProfModel, Entity
from path_in_IT_bot.readers.questions_reader import questions_list as questions

max_values = {}
for q in questions:
    for av in q.answers.values():
        for cr, points in av.items():
            if cr.lower() in max_values:
                max_values[cr.lower()] += points
            else:
                max_values[cr.lower()] = points

model = ProfModel.default()

states = StatesGroupBuilder(*[f"q{i}" for i in range(len(questions))] + ["result"]).build()

questions_with_answers: list[str] = []
for q in questions:
    question_with_answers = q.question + "\n"
    for i, a in enumerate(q.answers.keys()):
        question_with_answers += f'\n{i + 1}) {a}\n'
    questions_with_answers += [question_with_answers]


async def on_next_click(message: CallbackQuery, button: Button, manager: DialogManager):
    widget_id = 'm_' + manager.current_context().state.state[-3:].removeprefix('_')
    question_id = int(widget_id.removeprefix('m_q'))
    data = manager.current_context().widget_data

    for j, a in enumerate(questions[question_id].answers.keys()):
        if str(j) not in data[widget_id]:
            continue
        for cr, points in questions[question_id].answers[a].items():
            print(cr, points)
            manager.dialog_data[cr.lower()] += points
    print(data, widget_id, manager.dialog_data)

    if len(data[widget_id]) < 1:
        await message.answer("Нужно выбрать хотя бы один вариант ответа!")
    else:
        await manager.next()

    # for k, v in manager.current_context().widget_data.items():
    #     if k.startswith('m_q') and len(v) < 1:
    #         break


async def get_data(**_kwargs):
    return {
        q.question: tuple(str(i + 1) for i in range(len(q.answers.keys()))) for q in questions
    }


async def get_result_data(dialog_manager: DialogManager, **_kwargs):
    res = {
        k: dialog_manager.dialog_data[k]/dialog_manager.start_data[k] for k in max_values.keys()
        # "образы и визуализация": dialog_manager.dialog_data["образы и визуализация"],
        # "тексты и языки": dialog_manager.dialog_data["тексты и языки"],
        # "числа и вычисления": dialog_manager.dialog_data["числа и вычисления"],
        # "системы и механизмы": dialog_manager.dialog_data["системы и механизмы"],
        # "люди и взаимодействие": dialog_manager.dialog_data["люди и взаимодействие"],
        # "организация и управление": dialog_manager.dialog_data["организация и управление"],
        # "разработка и создание нового": dialog_manager.dialog_data["разработка и создание нового"],
        # "продвижение": dialog_manager.dialog_data["продвижение"],
        # "структурирование и контроль": dialog_manager.dialog_data["структурирование и контроль"],
        # "исследование и анализ": dialog_manager.dialog_data["исследование и анализ"]
    }

    res_sorted: list[tuple[str, float]] = list(res.items())
    res_sorted.sort(key=lambda x: x[1])
    res_to_ent = {k[0]: i+1 for i, k in enumerate(res_sorted)}
    print(res_to_ent)
    res_to_print = {k: v*dialog_manager.start_data[k] for k, v in res.items()}

    specs = model.position_of(Entity(res_to_ent))
    print(specs)
    opropriate_specs = f"{specs[0][0].name} {round(specs[0][1]*100, 3)}%"
    print(opropriate_specs)

    res_to_print["профригодность"] = opropriate_specs

    return res_to_print


windows: list[Window] = [
    Window(
        Const(questions_with_answers[0]),
        Multiselect(
            Format("✓ {item[0]}"),  # E.g `✓ Apple`
            Format("{item[0]}"),
            id="m_q0",
            # min_selected=1,
            item_id_getter=operator.itemgetter(0),
            items=questions[0].question,
        ),
        Button(Const("Следующий вопрос"), id='b', on_click=on_next_click),
        state=getattr(states, "state_q0"),
        getter=get_data,
    )
]
for i, q in enumerate(questions):
    if i in (0, len(questions) - 1):
        continue
    w: Window = Window(
        Const(questions_with_answers[i]),
        Multiselect(
            Format("✓ {item[0]}"),  # E.g `✓ Apple`
            Format("{item[0]}"),
            id=f"m_q{i}",
            # min_selected=1,
            item_id_getter=operator.itemgetter(0),
            items=q.question,
        ),
        Button(Const("Следующий вопрос"), id='b', on_click=on_next_click),
        Back(text=Const("Предыдущий вопрос")),
        state=getattr(states, f"state_q{i}"),
        getter=get_data,
    )

    windows += [w]

results = []
for k in max_values.keys():
    results += [Format(f"{k}: " + "{" + k + "}")]

# results = results[:5]
windows += [
    Window(
        Const(questions_with_answers[-1]),
        Multiselect(
            Format("✓ {item[0]}"),  # E.g `✓ Apple`
            Format("{item[0]}"),
            id=f"m_q{len(questions) - 1}",
            # min_selected=1,
            item_id_getter=operator.itemgetter(0),
            items=questions[-1].question,
        ),
        Button(Const("Закончить тест"), id='b', on_click=on_next_click),
        Back(text=Const("Предыдущий вопрос")),
        state=getattr(states, f"state_q{len(questions) - 1}"),
        getter=get_data,
    ),

    Window(
        Const("Твои результаты: "),
        *results,
        Format("\nПодходящая профессия: {профригодность}"),
        state=getattr(states, "state_result"),
        getter=get_result_data,
    )
]

router = Dialog(
    *windows
)


async def start(message: Message, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    print(max_values)
    await dialog_manager.start(getattr(states, "state_q0"), mode=StartMode.RESET_STACK, data=max_values)
    for k in max_values.keys():
        dialog_manager.dialog_data[k] = 0
