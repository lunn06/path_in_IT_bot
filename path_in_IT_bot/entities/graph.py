from __future__ import annotations

from abc import ABC
from copy import deepcopy
from typing import Any


class AbstractNode(ABC):
    _id: str
    _tags: dict[str, str]
    _text: str
    _branches: list[Edge]

    def __init__(self, node_id: str, tags: dict[str, str], text: str, branches: list[Edge] | None = None):
        self._id = node_id
        self._tags = tags
        self._text = text
        self._branches = branches if branches is not None else []

    @classmethod
    def from_data(cls, node_data: dict[str, Any]) -> AbstractNode:
        abs_node = cls(
            node_data["id"],
            node_data["tags"],
            node_data["text"],
            [],
        )

        return abs_node

    @property
    def id(self) -> str:
        return self._id

    @property
    def tags(self) -> dict[str, str]:
        return self._tags

    @property
    def text(self) -> str:
        return self._text

    @property
    def branches(self) -> list[Edge]:
        return self._branches

    @branches.setter
    def branches(self, branches: list[Edge]):
        self._branches = branches


class InitNode(AbstractNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class QuestionNode(AbstractNode):
    _answers: list[str | None]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._answers = []

    @property
    def answers(self) -> list[str | None]:
        return self._answers

    @answers.setter
    def answers(self, answer) -> None:
        self._answers = answer


class ChooseQuestionNode(QuestionNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EndNode(AbstractNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GraphBuilder:
    @staticmethod
    def node_build_from(node_data: dict[str, str]) -> AbstractNode:
        formatted_node_data: dict[str, Any] = deepcopy(node_data)
        split_text = node_data["text"].split("---")
        tags_str = split_text[1].split("\n")
        tags: dict[str, str] = {}
        # print(list(tags_str))
        for tag_str in tags_str:
            if not tag_str:
                continue
            tag, value = tag_str.split(":")
            tags[tag.strip()] = value.strip()
        # print(tags)
        formatted_text = split_text[2].strip()
        formatted_node_data["tags"] = tags
        formatted_node_data["text"] = formatted_text

        match formatted_node_data["tags"]["type"]:
            case "init":
                return InitNode.from_data(formatted_node_data)
            case "end":
                return EndNode.from_data(formatted_node_data)
            case "question":
                return QuestionNode.from_data(formatted_node_data)
            case "choose_question":
                return ChooseQuestionNode.from_data(formatted_node_data)
            case _:
                raise RuntimeError()

    @staticmethod
    def edges_from(nodes: dict[str, AbstractNode], edge_data: dict[str, str]):
        from_node_id = edge_data["fromNode"]
        to_node_id = edge_data["toNode"]
        label = edge_data.get("label", None)

        from_node = nodes[from_node_id]
        to_node = nodes[to_node_id]

        if isinstance(from_node, QuestionNode):
            question_node: QuestionNode = from_node
            if label:
                question_node.answers += [label]

        from_node.branches += [Edge(
            from_node,
            to_node,
            label,
        )]


class Edge:
    _from_node: AbstractNode
    _to_node: AbstractNode
    _label: str | None

    def __init__(self, from_node: AbstractNode, to_node: AbstractNode, label: str | None = None):
        self._from_node = from_node
        self._to_node = to_node
        self._label = label

    @property
    def from_node(self) -> AbstractNode:
        return self._from_node

    @property
    def to_node(self) -> AbstractNode:
        return self._to_node

    @property
    def label(self) -> str | None:
        return self._label


if __name__ == "__main__":
    GraphBuilder.node_build_from({"id": "123", "text": "\n---\ntype: init\ntest: 213\n---\nHello"})
