from aiogram.fsm.state import StatesGroup, State

from path_in_IT_bot.builders.states_group_builder import StatesGroupBuilder
from path_in_IT_bot.readers.questions_reader import questions


class MenuStates(StatesGroup):
    main = State()


ProftestStates = StatesGroupBuilder(*[f"q{i}" for i in range(len(questions))] + ["result"]).build()
