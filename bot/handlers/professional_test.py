import operator
from math import floor

from aiogram.enums import ContentType
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram.utils.formatting import Italic, Bold
from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Multiselect, Back, Button, Row, Start, Cancel
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const

from bot.builders.states_group_builder import StatesGroupBuilder
from bot.classificator import ProfModel, Entity
from bot.readers.questions_reader import questions_list as questions

questions = questions[:3]

max_values = {}
for q in questions:
    for av in q.answers.values():
        for cr, points in av.items():
            if cr.lower() in max_values:
                max_values[cr.lower()] += points
            else:
                max_values[cr.lower()] = points


class MenuStates(StatesGroup):
    main = State()


class Recommendations(StatesGroup):
    unimplemented = State()


recommendations_dialog = Dialog(
    Window(
        Const("Модуль не готов"),
        Cancel(Const("Назад")),
        state=Recommendations.unimplemented
    )
)


class Practice(StatesGroup):
    unimplemented = State()


practice_dialog = Dialog(
    Window(
        Const("Модуль не готов"),
        Cancel(Const("Назад")),
        state=Practice.unimplemented
    )
)

states = StatesGroupBuilder(*[f"q{i}" for i in range(len(questions))] + ["result"]).build()


# async def menu_start(callback: CallbackQuery, _button: Button, dialog_manager: DialogManager):
#     kb = [
#         [types.KeyboardButton(text="Тест на профориентацию")]
#     ]
#
#     keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
#     await dialog_manager.done()
#     await dialog_manager.start(MenuStates.main)


async def proftest_first_start(message: Message, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(getattr(states, "state_q0"), mode=StartMode.RESET_STACK, data=max_values)
    for k in max_values.keys():
        dialog_manager.dialog_data[k] = 0


async def proftest_from_button_start(callback: CallbackQuery, button: Start, manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    await manager.start(state=button.state, data=button.start_data, show_mode=button.mode)
    # await dialog_manager.start(getattr(states, "state_q0"), mode=StartMode.NORMAL, data=max_values)
    for k in max_values.keys():
        manager.dialog_data[k] = 0


def message_approve(text):
    def f(msg_text):
        if msg_text == text:
            return True
        raise ValueError

    return f


async def unexpected_message(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    await message.answer(text='Такого раздела нет!')


windows: list[Window] = []

curses_window = Window(
    Const("Добро пожаловать!"),
    # TextInput(
    #     id="proftest",
    #     type_factory=message_approve("Тест на профориентацию"),
    #     on_success=proftest_start,
    #     on_error=unexpected_message,
    # ),
    Start(
        Const("Тест на профориентацию"),
        id="123",
        state=states.state_q0,
        # on_click=proftest_from_button_start,
        data=max_values,
    ),
    Start(
        Const("Рекомендации"),
        id="1",
        state=Recommendations.unimplemented,
    ),
    Start(
        Const("Практикум"),
        id="2",
        state=Practice.unimplemented,
    ),
    markup_factory=ReplyKeyboardFactory(resize_keyboard=True, one_time_keyboard=True),
    state=MenuStates.main,
)

windows += [curses_window]

menu_dialog = Dialog(*windows)

model = ProfModel.default()

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
            if cr.lower() in manager.dialog_data.keys():
                manager.dialog_data[cr.lower()] += points
            else:
                manager.dialog_data[cr.lower()] = points
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
        q.question: tuple((str(i + 1), list(q.answers.keys())[i]) for i in range(len(q.answers.keys()))) for q in
        questions
    }


async def get_result_data(dialog_manager: DialogManager, **_kwargs):
    for k in dialog_manager.start_data.keys():
        dialog_manager.dialog_data[k] = dialog_manager.dialog_data.get(k, 0)
    res = dialog_manager.dialog_data
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
    # }

    res_sorted: list[tuple[str, float]] = list(res.items())
    res_sorted.sort(key=lambda x: x[1])
    # print(res_to_ent)
    # res_to_print = {k: Italic(v * dialog_manager.start_data[k]).as_markdown().replace('\\', '') for k, v in res.items()}
    res_to_ent = {}
    res_to_print = {}
    max_values = dialog_manager.start_data
    max_points = max(max_values.values())
    for i, t in enumerate(res_sorted):
        k, v = t
        res_to_ent[k] = i + 1
        scale = floor(max_points / max_values[k])
        scaled_proc = round(v / max_values[k] * scale * 100, 2)
        scaled_proc_floor = scaled_proc if scaled_proc < 100 else 100
        res_to_print[k] = Italic(scaled_proc_floor).as_markdown().replace('\\', '')

    specs = model.position_of(Entity(res_to_ent))
    opropriate_name = Bold(specs[0][0].name).as_markdown().replace('\\', '')
    opropriate_proc = round(specs[0][1] * 100, 3)

    template = f'''
Твои результаты: 
⚙️ Системы и механизмы: {res_to_print['системы и механизмы']}%
🧮 Числа и вычисления: {res_to_print['числа и вычисления']}%
🎑 Образы и визуализация: {res_to_print['образы и визуализация']}%
🤝 Люди и взаимодействие: {res_to_print['люди и взаимодействие']}%
📜 Тексты и языки: {res_to_print['тексты и языки']}%
📣 Организация и управление: {res_to_print['организация и управление']}%
📈 Продвижение: {res_to_print['продвижение']}%
💡 Разработка и создание нового: {res_to_print['разработка и создание нового']}%
🏰Структурирование и контроль: {res_to_print['структурирование и контроль']}%
🧑‍🔬 Исследование и анализ: {res_to_print['исследование и анализ']}%

'''
    template += (Bold(f"Подходящая профессия: {opropriate_name}. Она походит тебе на {opropriate_proc}%").as_markdown()
                 .replace("\\", ''))
    res_to_print["профпригодность"] = template

    print(res_to_print)

    return res_to_print


windows: list[Window] = []
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
    state=getattr(states, "state_q0"),
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
        state=getattr(states, f"state_q{i}"),
        getter=get_data,
    )]

results = []
for k in max_values.keys():
    results += [Format(f"{k}: " + "{" + k + "}")]

# results = results[:5]
if questions[-1].image is not None:
    windows += [
        Window(
            StaticMedia(
                path=questions[-1].image,
                type=ContentType.PHOTO
            ),
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
            state=getattr(states, f"state_q{len(questions) - 1}"),
            getter=get_data,
        ),

    ]
else:
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
            Row(
                Back(text=Const("Предыдущий вопрос")),
                Button(Const("Закончить тест"), id='b', on_click=on_next_click),
            ),
            state=getattr(states, f"state_q{len(questions) - 1}"),
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
        state=MenuStates.main,
        mode=StartMode.RESET_STACK
    ),
    state=getattr(states, "state_result"),
    getter=get_result_data,
)

windows += [result]

proftest_dialog = Dialog(
    *windows
)
