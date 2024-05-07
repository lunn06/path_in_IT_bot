from aiogram.fsm.state import StatesGroup, State

from bot.builders.states_group_builder import StatesGroupBuilder
from bot.readers.questions_reader import questions


class MenuStates(StatesGroup):
    main = State()


ProftestStates = StatesGroupBuilder(*[f"q{i}" for i in range(len(questions))] + ["result"]).build()
