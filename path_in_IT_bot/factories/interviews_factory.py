import os
from glob import glob

from path_in_IT_bot.entities.interveiw import Interview
from path_in_IT_bot.factories.abstract_factory import AbstractFactory


class InterviewsFactory(AbstractFactory):
    def __init__(self, interviews_path: str):
        if not os.path.exists(interviews_path):
            raise ValueError("Interviews path is not exist")

        self.interviews_path = interviews_path
        if not interviews_path.endswith(os.sep + "*"):
            self.interviews_path += os.sep + "*"

        self._items = [Interview(interview_path) for interview_path in glob(self.interviews_path)]

    @property
    def items(self) -> list[Interview]:
        return self._items


if __name__ == "__main__":
    from path_in_IT_bot.utils import iter_graph

    factory = InterviewsFactory("/home/dcdnc/mycod/python/path_in_IT_bot/models/interviews")
    for interview in factory.items:
        print(interview.name)
        for node in iter_graph(interview.root):
            print(node.text, list((branch.label, branch.to_node.text) for branch in node.branches))
