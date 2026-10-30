import json
from pathlib import Path


def main():
    result = json.loads(Path("summary.json").read_text())
    report = (
        "# Example result\n\n"
        f"The selected values sum to {result['selected_sum']}.\n\n"
        f"Expected records: {result['expected_count']}\n\n"
        f"Selected records: {len(result['selected_ids'])}\n\n"
        f"Missing records: {len(result['missing_ids'])}\n\n"
        f"Excluded records: {len(result['excluded_ids'])}\n\n"
        f"Minimum value: {result['minimum_value']}\n"
    )
    Path("report.md").write_text(report)


if __name__ == "__main__":
    main()
