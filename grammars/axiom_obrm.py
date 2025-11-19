import os
import json
from source.cfg_utils import Rule

obrm_base = [] # TODO

obrm = list(obrm_base)
seen_rules = set()

# Load lexical item grammar rules
rule_files = []

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
                obrm.append(r)
