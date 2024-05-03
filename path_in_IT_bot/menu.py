from aiogram.fsm.state import State, StatesGroup


class Menu(StatesGroup):
    home = State()
    test = State()
    garage = State()
    kitchen = State()
    wardrobe = State()
    interview = State()
