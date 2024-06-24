def prepare_model(model: dict[str, float]) -> dict[str, int]:
    prepared = sorted(model.keys(), key=lambda x: model[x])

    return {k: i + 1 for i, k in enumerate(prepared)}
