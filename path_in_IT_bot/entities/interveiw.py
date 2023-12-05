import os
import json
from typing import Any
from shutil import copyfile

from path_in_IT_bot.utils import iter_graph
from path_in_IT_bot.entities.graph import GraphBuilder, AbstractNode, InitNode


class Interview:
    _path: str
    _name: str
    _json: dict[str, Any]
    _root: AbstractNode
    _nodes: list[AbstractNode]

    files_dir = ".cache"

    def __init__(self, path: str):
        # if path.strip().endswith(".canvas"):
        #     file_name = list(path.strip().split(os.sep))[-1]
        #     json_dir = os.getcwd() + os.sep + Interview.files_dir
        #     if not os.path.exists(json_dir):
        #         os.mkdir(json_dir)
        #     json_file = file_name.replace(".canvas", ".json")
        #     json_path = json_dir + os.sep + json_file
        #     copyfile(path, json_path)
        #
        #     self._path = json_path
        # elif path.strip().endswith(".json"):
        #     self._path = path
        # else:
        #     raise ValueError("Path is not valid")

        # self._name: str = self._path.strip().split("/")[-1].removesuffix(".json")
        self._path = path
        self._name: str = self._path.strip().split("/")[-1].removesuffix(".canvas")

        with open(self._path) as file:
            self._json = json.loads(file.read())

        # self._nodes: list[AbstractNode] = []
        self._build_graph()

    # @property
    # def nodes(self) -> list[AbstractNode]:
    #     return self._nodes

    @property
    def name(self) -> str:
        return self._name

    @property
    def root(self) -> AbstractNode:
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
    interview = Interview("/home/dcdnc/mycod/python/path_in_IT_bot/models/interviews/Test.canvas")
    print(interview.name)
    for node in iter_graph(interview.root):
        print(node.text, list((branch.label, branch.to_node.text) for branch in node.branches))
