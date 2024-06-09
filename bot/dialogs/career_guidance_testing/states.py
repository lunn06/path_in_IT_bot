from aiogram.fsm.state import StatesGroup, State

class MenuStates(StatesGroup):
    main = State()

class GreetingStates(StatesGroup):
    main = State()

class Recommendations(StatesGroup):
    unimplemented = State()

class Practice(StatesGroup):
    unimplemented = State()