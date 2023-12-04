from aiogram.fsm.state import State, StatesGroup


class Menu(StatesGroup):
    garage = State()
    kitchen = State()
    wardrobe = State()
    interview = State()
