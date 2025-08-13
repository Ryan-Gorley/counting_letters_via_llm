import itertools
import json


from pathlib import Path
from typing import TypedDict

from llm_testing import ExperimentData

SAMPLE_FOLDER = Path("results")
EXPERIMENT_DATA = ExperimentData(refusals=[], successes=[])

for file in SAMPLE_FOLDER.glob("*.json"):
    with open(file, "r") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        continue
    EXPERIMENT_DATA["refusals"].extend(data.get("refusals", []))
    EXPERIMENT_DATA["successes"].extend(data.get("successes", []))

structured_data: dict[str, dict[str, list[int]]] = {}

TOTAL_CORRECT = 0
TOTAL_WRONG = 0

for sample in EXPERIMENT_DATA["successes"]:
    word, letter, count = sample
    structured_data.setdefault(word, {}).setdefault(letter, []).append(count)
    if word.count(letter) == count:
        TOTAL_CORRECT += 1
    else:
        TOTAL_WRONG += 1

# Sort samples
for word, by_letter in structured_data.items():
    for letter in by_letter:
        by_letter[letter].sort()


def print_totals():
    print(f"Total correct: {TOTAL_CORRECT}")
    print(f"Total wrong: {TOTAL_WRONG}")


def print_all():
    import pprint
    pprint.pprint(structured_data)