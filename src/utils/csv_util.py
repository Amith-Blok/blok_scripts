import csv


def csv_to_list(path: str, skip_subheader: bool = True) -> list:
    try:
        with open(path, "r", encoding="utf-8") as file:
            header = next(file)
            if skip_subheader:
                next(file)  # skip second row sub heading
            reader = csv.DictReader(
                file, fieldnames=[h.strip() for h in header.strip().split(",")]
            )
            return list(reader)
    except Exception as e:
        print(f"Error reading csv file: {e}")
        return []


def write_data_csv(path: str, records: list, headers: list[str]):
    with open(path, "w", encoding="utf-8", newline="") as file:
        write = csv.DictWriter(file, fieldnames=headers)
        write.writeheader()
        write.writerows(records)
