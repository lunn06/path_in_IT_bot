import json
import os
from typing import Any

from path_in_IT_bot.entities.graph import GraphBuilder, InitNode
from path_in_IT_bot.utils import iter_graph


class Interview:
    _path: str
    _name: str
    _json: dict[str, Any]
    _root: InitNode

    files_dir = ".cache"

    def __init__(self, path: str):
        self._path = path
        self._name: str = self._path.strip().split(os.sep)[-1].removesuffix(".canvas")

        with open(self._path) as file:
            self._json = json.loads(file.read())

        self._build_graph()

    @property
    def name(self) -> str:
        return self._name

    @property
    def root(self) -> InitNode:
        return self._root

    def _build_graph(self) -> None:
        nodes = {}
        for node_data in self._json["nodes"]:
            graph_node = GraphBuilder.node_build_from(node_data)
            nodes[node_data["id"]] = graph_node

            if isinstance(graph_node, InitNode):
                self._root = graph_node

        for edge_data in self._json["edges"]:
            GraphBuilder.edges_from(nodes, edge_data)
        # self._nodes = list(nodes.values())


if __name__ == "__main__":
    interview = Interview("/models/Test.canvas")
    print(interview.name)
    for node in iter_graph(interview.root):
        print(node.text, list((branch.label, branch.to_node.text) for branch in node.branches))
