import json
from pathlib import Path


def main():
    records = json.loads(Path("input.json").read_text())
    minimum = json.loads(Path("params.json").read_text())["minimum_value"]
    selected = []
    missing = []
    excluded = []
    identifiers = set()

    for record in records:
        identifier = record["id"]
        if identifier in identifiers:
            raise ValueError(f"Duplicate identifier: {identifier}")
        identifiers.add(identifier)
        value = record["value"]
        if value is None:
            missing.append(identifier)
        elif type(value) is not int:
            raise ValueError(f"Expected an integer or null: {identifier}")
        elif value < minimum:
            excluded.append(identifier)
        else:
            selected.append(record)

    result = {
        "expected_count": len(records),
        "selected_ids": [record["id"] for record in selected],
        "selected_sum": sum(record["value"] for record in selected),
        "missing_ids": missing,
        "excluded_ids": excluded,
        "minimum_value": minimum,
    }
    Path("summary.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
