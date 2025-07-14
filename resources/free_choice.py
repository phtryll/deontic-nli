import os
import json
from source.cfg_utils import Rule

fcp_base = [

    Rule(left="S", right=["<PREMISE>", "<HYPOTHESIS>"], features={'subj':'?x'}),

    Rule(left="<PREMISE>", right=["<PROPOSITION>"]),
    Rule(left="<HYPOTHESIS>", right=["<PROPOSITION>"]),
    Rule(left="<PROPOSITION>", right=["A"]),
    Rule(left="<PROPOSITION>", right=["B"]),
    Rule(left="A", right=["NP", "VP", "."]),
    Rule(left="B", right=["NP", "VP", "."]),



    

    # Rule(
    #     left="<PREMISE>",
    #     right=["[P]", "PE", "COMP", "p", "or", "q", "."],
    # ),

    # Rule(
    #     left="<HYPOTHESIS>",
    #     right=["[H]", "PE", "COMP", "p", "and", "PE", "COMP", "q", "."],
    # ),

    # Rule(
    #     left="<PREMISE>",
    #     right=["[P]", "PE", "COMP", "PROP", "."],
    # ),

    # Rule(
    #     left="<HYPOTHESIS>",
    #     right=["[H]", "PE", "COMP", "PROP", "."],
    # ),

    # Rule(
    #     left="<HYPOTHESIS>",
    #     right=["[H]", "PE", "COMP", "p", "or", "q", "."],
    # ),

    # Rule(
    #     left="<PREMISE>",
    #     right=["[P]", "p", "or", "q"],
    # ),

    # Rule(
    #     left="<HYPOTHESIS>",
    #     right=["[H]", "p", "or", "q"],
    # ),

    # Rule(
    #     left="<PREMISE>",
    #     right=["[P]", "p", "and", "q"],
    # ),

    # Rule(
    #     left="<HYPOTHESIS>",
    #     right=["[H]", "p", "and", "q"],
    # ),

    # Rule(
    #     left="<HYPOTHESIS>",
    #     right=["[H]", "PROP"],
    # ),

    # Rule(
    #     left="<PREMISE>",
    #     right=["[P]", "PROP"],
    # ),

    # Rule(left="PE", right=["it is", "NEG", "permitted"]),
    # Rule(left="NEG", right=["not"]),
    # Rule(left="NEG", right=[""]),
    
    # Rule(left="COMP", right=["that"]),

    # Rule(left="PROP", right=["p"]),
    # Rule(left="PROP", right=["q"]),
    # Rule(left="p", right=["A"]),
    # Rule(left="q", right=["B"])
]

fcp = list(fcp_base)
seen_rules = set()

# Load lexical item grammar rules
rule_files = [
    "rules_NP.json",
    "rules_VP.json"
]

# Add them to the grammar
for file in rule_files:
    rules_path = os.path.join(os.path.dirname(__file__), '..', 'data', file)
    
    # Extract rules
    with open(rules_path, 'r') as json_file:
        rules = json.load(json_file)
    
    # Add rules to rules list
    for rules_list in rules.values():
        for entry in rules_list:
            r = eval(entry)
            if r not in seen_rules:
                seen_rules.add(r)
                fcp.append(r)

# Add relevant features
for rule in fcp:
    if rule.left == "NP":
        rule.features.setdefault("subj", rule.right[0])
