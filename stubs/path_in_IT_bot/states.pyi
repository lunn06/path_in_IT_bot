from _typeshed import Incomplete
from aiogram.fsm.state import StatesGroup
from path_in_IT_bot.readers.model_reader import model as model

class Menu(StatesGroup):
    main_menu: Incomplete
    @classmethod
    def initialize(cls) -> None: ...
