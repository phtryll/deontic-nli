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


def format_rules(slot_dict: Dict[str, List[str]]) -> Dict[str, List[Rule]]:
    rules_map: Dict[str, List[Rule]] = {}

    for slot_label, items in slot_dict.items():
        rules: List[Rule] = []
        
        for item in items:
            rules.append(Rule(left=slot_label, right=[item]))

        rules_map[slot_label] = rules
    
    return rules_map