# from typing import Type
#
# from aiogram.fsm.state import StatesGroup
# from aiogram_dialog import Window, Dialog
# from aiogram_dialog.widgets.kbd import Button
# from aiogram_dialog.widgets.text import Const
#
# from path_in_IT_bot.readers.model_reader import model
# from path_in_IT_bot.builders.states_builder import StatesGroupBuilder
#
# menu: Type[StatesGroup] = StatesGroupBuilder.build_from(
#     ["main_menu"] + [prod for prod in model.producers.keys()]
# )
#
# windows: list[Window] = [
#     Window(
#         Const("Привет\nКак жизнь?"),
#         Button(Const("Пуск!"), id="nothing"),
#         state=getattr(menu, "main_menu")
#     )
# ]
# for producer in model.producers.keys():
#     window: Window = Window(
#         Const(f"Добро пожаловать в {producer.capitalize()}"),
#         Button(Const("Что?"), id="nothing"),
#         state=getattr(menu, producer)
#     )
#
#     windows.append(window)
#
# dialog = Dialog(*windows)
