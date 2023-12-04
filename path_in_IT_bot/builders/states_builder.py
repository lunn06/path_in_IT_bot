from typing import Type

from aiogram.fsm.state import StatesGroup, State  # noqa: F401
from jinja2.nativetypes import NativeEnvironment

from path_in_IT_bot.utils import random_str

meta_class_template = '''
class Meta_{{ class_id }}(StatesGroup):
{% for state_id in states %}
    state_{{ state_id }} = State()
{% endfor %}
'''


class StatesGroupBuilder:

    def __init__(self, *states: str):
        """

        :type Iterable[str] states: object
        """

        self._states: list[str] = list(states)

    @staticmethod
    def build_from(*entity: str) -> Type[StatesGroup]:
        builder = StatesGroupBuilder(*entity)
        return builder.build()

    def add(self, *states) -> None:
        self._states.extend(states)

    def remove(self, target: str) -> None:
        if target in self._states:
            self._states.remove(target)

    def build(self) -> Type[StatesGroup]:
        states: list[str] = self._states

        env = NativeEnvironment()
        # env = Environment()
        t = env.from_string(meta_class_template)
        uuid = random_str(5)
        render = t.render(states=states, class_id=uuid)
        exec(render)

        # class Meta(StatesGroup):
        #     @classmethod
        #     def insert_states(cls):
        #         for state_name in states:
        #             state = State(state=state_name)
        #             state._group = cls
        #             setattr(cls, state_name, state)
        #
        # Meta.insert_states()
        # return Meta

        return eval(f"Meta_{uuid}")


if __name__ == "__main__":
    res = StatesGroupBuilder.build_from(*["a", "b", "c"])
    print(dir(res))
    print(type(res))
    print(res)
