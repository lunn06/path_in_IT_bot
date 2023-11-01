from typing import Type

from aiogram.fsm.state import StatesGroup
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Const

from path_in_IT_bot.readers.model_reader import model
from path_in_IT_bot.factories.states_builder import StatesGroupBuilder

builder = StatesGroupBuilder(
    ["main_menu"] + [prod for prod in model.producers.keys()]
)
Menu: Type[StatesGroup] = builder.build()

windows: list[Window] = [
    Window(
        Const("Привет\nКак жизнь?"),
        Button(Const("Пуск!"), id="nothing"),
        state=getattr(Menu, "main_menu")
    )
]
for producer in model.producers.keys():
    window: Window = Window(
        Const(f"Добро пожаловать в {producer.capitalize()}"),
        Button(Const("Что?"), id="nothing"),
        state=getattr(Menu, producer)
    )

    windows.append(window)

dialog = Dialog(*windows)
