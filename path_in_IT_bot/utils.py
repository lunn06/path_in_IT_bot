from typing import Generator

from aiogram.types import KeyboardButton

from path_in_IT_bot.readers.model_reader import model


def build_main_menu_kb() -> list[list[KeyboardButton]]:
    return [
        [KeyboardButton(text=producer_value.translate.capitalize())] for producer_value in model.producers.values()
    ]
