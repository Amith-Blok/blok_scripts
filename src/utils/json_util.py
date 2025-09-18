from json import dump, load


def write_data_json(path: str, records: list[dict]):
    with open(path, "w", encoding="utf-8") as file:
        dump(records, file, indent=4)


def load_json(path: str):

    result = []
    with open(path, encoding="utf-8") as file:
        result = load(file)
    if not result:
        raise ValueError("Wrong path for load_json path:", path)
    return result
