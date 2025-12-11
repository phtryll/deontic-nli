from source.cfg_utils import Rule
from typing import List, Dict


def format_examples(input: Dict[str, List[str]]) -> Dict[str, List[tuple[str, str]]]:
    formatted_examples: Dict[str, List[tuple[str, str]]] = {}

    for grammar, examples in input.items():
        formatted_examples[grammar] = []

        for example in examples:
            if "[H]" in example:
                premise, hypothesis = example.split("[H]", 1)
                premise = premise.replace("[P]", "", 1).strip()
                hypothesis = hypothesis.strip()
                formatted_examples[grammar].append((premise, hypothesis))
    
    return formatted_examples


def format_rules(data: Dict[str, List]) -> Dict[str, List[Rule]]:
    rules_map: Dict[str, List[Rule]] = {}

    fields = data["fields"]
    items = data["items"]

    for col_idx, field in enumerate(fields):
        rules: List[Rule] = []
        for row in items:
            rules.append(Rule(left=field, right=[row[col_idx]]))
        rules_map[field] = rules

    return rules_map