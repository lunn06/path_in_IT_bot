from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from pydantic import BaseModel
from pydantic_core import from_json

from bot.configs import Config, parse_config
from bot.configs.questions import Quality


class Entities(BaseModel):
    entities: list["Entity"]


class Entity(BaseModel):
    name: str
    qualities: list["Quality"]


@lru_cache(maxsize=1)
def parse_entity(config: Config) -> Entities:
    entity_path = _entity_path(str(config.models_path))
    prepared_entity_json = _prepare_json(entity_path)
    # pprint(prepared_entity_json)
    entities = Entities.model_validate(prepared_entity_json)

    return entities


def _entity_path(models_path: str) -> str:
    return models_path + os.sep + "entities.json"


def _prepare_json(entity_path: str) -> dict[Any, Any]:
    with open(entity_path, 'r') as entity_file:
        entity_json = from_json(entity_file.read())

    prepared_json: dict[str, Any] = {"entities": []}
    for entity, qualities_dict in entity_json.items():
        entity_dict = {
            "name": entity,
            "qualities": [],
        }
        for quality, points in qualities_dict.items():
            entity_dict["qualities"] += [{
                "name": quality.lower(),
                "points": points,
            }]
        prepared_json["entities"] += [entity_dict]

    return prepared_json


if __name__ == '__main__':
    config = parse_config()
    entities = parse_entity(config)
    print(entities)
