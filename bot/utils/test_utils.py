def top_max_pairs(data: dict, maxPairs: int) -> dict:
    sorted_pairs = sorted(data.items(), key=lambda item: item[1], reverse=True)
    top_three_pairs = sorted_pairs[:min(maxPairs, len(sorted_pairs))]
    result = dict(top_three_pairs)
    return result


