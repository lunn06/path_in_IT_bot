from aiogram.fsm.state import StatesGroup, State


class Menu(StatesGroup):
    main_menu = State()
    garage = State()
    checkroom = State()
    kitchen = State()
    interviews = State()