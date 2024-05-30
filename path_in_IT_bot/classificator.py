import json


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
            d = distance_between(c, cc)
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
        with (open("models/entities.json", 'r') as f):
            entities_dict = json.load(f)
            entities = []
            for name in entities_dict.keys():
                entities += [Entity(entities_dict[name], name)]

        return cls(entities)


def distance_between(ent1, ent2):
    return sum((float(ent1[i]) - float(ent2[i])) ** 2 for i in range(len(ent1))) ** 0.5


def main():
    with (open("/models/entities.json", 'r') as f):
        entities_dict = json.load(f)
        entities = []
        for name in entities_dict.keys():
            entities += [Entity(entities_dict[name], name)]

    model = ProfModel(entities)

    test_entity = Entity({
        "образы и визуализация": 7,
        "тексты и языки": 8,
        "числа и вычисления": 4,
        "системы и механизмы": 3,
        "люди и взаимодействие": 5,
        "организация и управление": 9,
        "разработка и создание нового": 1,
        "продвижение": 10,
        "структурирование и контроль": 2,
        "исследование и анализ": 6
    }, "Test")

    res = model.position_of(test_entity)

    print(f"Для модели {test_entity.name}:")
    for e, r in res:
        print(f"\t{e.name} - {round(r * 100, 2)}%")


if __name__ == "__main__":
    main()
