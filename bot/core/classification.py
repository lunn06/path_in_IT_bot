import json
import os

from bot.configs.config import parse_config


class Entity:
    def __init__(self, ent: dict[str, int], name=None):
        self.name = name
        self.ent = ent


class ProfModel:
    entities: list[Entity]

    def __init__(self, entities: list[Entity]):
        self.entities = entities

    def position_of(self, ent: Entity) -> tuple[tuple[Entity, float]]:
        cc = tuple(ent.ent[k] for k in sorted(ent.ent.keys()))

        distances: list[tuple[Entity, float]] = []
        for e in self.entities:
            c = tuple(e.ent[k] for k in sorted(e.ent.keys()))
            d = ProfModel.distance_between(c, cc)
            distances += [(e, d)]

        distances.sort(key=lambda x: x[1])

        # noinspection PyTypeChecker
        normal_distances: tuple[float] = tuple(
            map(
                lambda x: (x[0], round(1 - x[1] / distances[-1][1], 3)),
                distances
            )
        )

        # noinspection PyTypeChecker
        return normal_distances

    @classmethod
    def default(cls):
        config = parse_config()
        with (open(str(config.models_path) + os.sep + "entities.json", 'r') as f):
            entities_dict = json.load(f)
            entities = []
            for name in entities_dict.keys():
                entities += [Entity(entities_dict[name], name)]

        return cls(entities)

    @staticmethod
    def distance_between(ent1, ent2):
        return sum((float(ent1[i]) - float(ent2[i])) ** 2 for i in range(len(ent1))) ** 0.5
