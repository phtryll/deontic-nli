import os
import json
from copy import deepcopy
from source.cfg_utils import Rule
from source.generate import parse_json

# ------------------------------------
# Free-choice permission test grammars
# ------------------------------------

A_or_B_impl_AB = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "PROP", "."]),

    Rule(left="PROP", right=["A"]),
    Rule(left="PROP", right=["B"]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a'}),
    Rule(left="B", right=["V_3SG"], features={'verb':'?b'}),
]

AB_impl_A_or_B = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "PROP", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "A", "or", "B", "."]),

    Rule(left="PROP", right=["A"]),
    Rule(left="PROP", right=["B"]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a'}),
    Rule(left="B", right=["V_3SG"], features={'verb':'?b'}),
]

A_or_B_impl_A_and_B = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "A", "and", "B", "."]),

    Rule(left="PROP", right=["A"]),
    Rule(left="PROP", right=["B"]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a'}),
    Rule(left="B", right=["V_3SG"], features={'verb':'?b'}),
]

A_and_B_impl_A_or_B = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "A", "and", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "A", "or", "B", "."]),

    Rule(left="PROP", right=["A"]),
    Rule(left="PROP", right=["B"]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a'}),
    Rule(left="B", right=["V_3SG"], features={'verb':'?b'}),
]

PE_A_or_B_impl_PE_A_and_PE_B = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "and", "is permitted to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),
]

PE_A_or_B_impl_PE_X = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "PROP", "."]),

    Rule(left="PROP", right=["A"]),
    Rule(left="PROP", right=["B"]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),
]

PE_A_or_B_impl_PE_A_or_PE_B = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "or", "is permitted to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),
]

PE_A_and_B_impl_PE_A_and_PE_B = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "and", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "and", "is permitted to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),
]

PE_A_and_B_impl_PE_A_and_B = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "and", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),
]

PE_A_or_PE_B_impl_PE_A_or_B = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "is permitted to", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),
]

PE_A_and_PE_B_impl_PE_A_and_B = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "and", "is permitted to", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "and", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),
]


PE_A_or_B_impl_neg_PE_A_and_PE_B_explicit = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["NEG", "SUBJ", "is both permitted to", "A", "and", "permitted to", "B", "."]),

    Rule(left="NEG", right=["it is not the case that"]),
    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),
]

PE_A_or_B_impl_neg_PE_X = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["NEG", "SUBJ", "is permitted to", "PROP", "."]),

    Rule(left="PROP", right=["A"]),
    Rule(left="PROP", right=["B"]),

    Rule(left="NEG", right=["it is not the case that"]),
    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),
]

PE_A_or_B_impl_neg_PE_A_and_PE_B_implicit = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "XA", "or", "XB", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "YA", "and", "is permitted to", "YB", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),

    Rule(left="XA", right=["A"], features={'ant':'n'}),
    Rule(left="YA", right=["A"], features={'ant':'y'}),
    
    Rule(left="XB", right=["B"], features={'ant':'n'}),
    Rule(left="YB", right=["B"], features={'ant':'y'}),

    Rule(left="A", right=["V_INF_neg"], features={'verb':'?a', 'ant':'n'}),
    Rule(left="B", right=["V_INF_neg"], features={'verb':'?b', 'ant':'n'}),

    Rule(left="A", right=["V_INF_ant"], features={'verb':'?a', 'ant':'y'}),
    Rule(left="B", right=["V_INF_ant"], features={'verb':'?b', 'ant':'y'}),
]

PE_A_or_B_impl_neg_PE_X_implicit = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "XA", "or", "XB", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "Y", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),

    Rule(left="XA", right=["A"], features={'ant':'n'}),
    Rule(left="XB", right=["B"], features={'ant':'n'}),

    Rule(left="Y", right=["A"], features={'ant':'y'}),
    Rule(left="Y", right=["B"], features={'ant':'y'}),

    Rule(left="A", right=["V_INF_neg"], features={'verb':'?a', 'ant':'n'}),
    Rule(left="B", right=["V_INF_neg"], features={'verb':'?b', 'ant':'n'}),

    Rule(left="A", right=["V_INF_ant"], features={'verb':'?a', 'ant':'y'}),
    Rule(left="B", right=["V_INF_ant"], features={'verb':'?b', 'ant':'y'}),
]

A_implies_neg_A_explicit_1 = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "A", "."]),
    Rule(left="<HYPOTHESIS>", right=["NEG", "SUBJ", "A", "."]),

    Rule(left="NEG", right=["it is not the case that"]),
    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a'}),
]

A_implies_neg_A_explicit_2 = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "XA", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "NEG", "YA", "."]),

    Rule(left="NEG", right=["doesn't"]),
    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="XA", right=["A"], features={'p':'y'}),
    Rule(left="YA", right=["A"], features={'p':'n'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a', 'p':'y'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a', 'p':'n'}),
]

A_implies_neg_V_explicit_1 = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "A", "."]),
    Rule(left="<HYPOTHESIS>", right=["NEG", "SUBJ", "B", "."]),

    Rule(left="NEG", right=["it is not the case that"]),
    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a'}),
    Rule(left="B", right=["V_3SG"], features={'verb':'?a'}),
]

A_implies_neg_V_explicit_2 = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "A", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "NEG", "B", "."]),

    Rule(left="NEG", right=["doesn't"]),
    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?a'}),
]

A_implies_not_not_A_1 = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "XA", "."]),
    Rule(left="<HYPOTHESIS>", right=["NEG", "SUBJ", "YA", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="NEG", right=["it is not the case that"]),

    Rule(left="XA", right=["A"], features={'ant':'n'}),
    Rule(left="YA", right=["A"], features={'ant':'y'}),

    Rule(left="A", right=["V_3SG_neg"], features={'verb':'?a', 'ant':'n'}),
    Rule(left="A", right=["V_3SG_ant"], features={'verb':'?a', 'ant':'y'}),
]

A_implies_not_not_A_2 = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "XA", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "NEG", "YA", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="NEG", right=["doesn't"]),

    Rule(left="XA", right=["A"], features={'ant':'n'}),
    Rule(left="YA", right=["A"], features={'ant':'y'}),

    Rule(left="A", right=["V_3SG_neg"], features={'verb':'?a', 'ant':'n'}),
    Rule(left="A", right=["V_INF_ant"], features={'verb':'?a', 'ant':'y'}),
]

PE_A_or_B_impl_PE_A_and_FO_B = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "and", "is forbidden to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),
]

PE_A_or_B_impl_FO_A_and_PE_B = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is forbidden to", "A", "and", "is permitted to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),
]

PE_A_or_B_impl_FO_A_or_FO_B = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is forbidden to", "A", "or", "is forbidden to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),
]

PE_A_and_B_impl_PE_A_or_FO_B = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "and", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "or", "is forbidden to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),
]

PE_A_and_B_impl_FO_A_or_PE_B = [
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "and", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is forbidden to", "A", "or", "is permitted to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),
]

# Group all test grammars in a dictionary
fcp_base = {
    name: val
    for name, val in locals().items()
    if isinstance(val, list) and all(isinstance(x, Rule) for x in val)
}

# -------------------------------------
# Load lexical rules and build features
# -------------------------------------

from collections import defaultdict

# Load lexical item grammar rules
rule_files = [
    "rules_NP.json",
    "rules_VP.json",
    "rules_VP_NEG.json"
]

# Group lexical rules by their left-hand category (e.g., "V_INF", "V_3SG", ...)
lexical_rules = defaultdict(list)

# Add them to the grammar (merge rules from all files)
for filename in rule_files:
    rules_path = os.path.join(os.path.dirname(__file__), 'data', filename)
    
    with open(rules_path, 'r') as json_file:
        data = json.load(json_file)
        
        for category, entries in data.items():
            for string in entries:
                rule = parse_json(string)
                lexical_rules[category].append(rule)

# Build lists of corresponding forms (take the first RHS token for each rule)
v_inf_list      = [r.right[0] for r in lexical_rules.get("V_INF", [])]
v_3sg_list      = [r.right[0] for r in lexical_rules.get("V_3SG", [])]
v_inf_neg_list  = [r.right[0] for r in lexical_rules.get("V_INF_neg", [])]
v_inf_ant_list  = [r.right[0] for r in lexical_rules.get("V_INF_ant", [])]
v_3sg_neg_list  = [r.right[0] for r in lexical_rules.get("V_3SG_neg", [])]
v_3sg_ant_list  = [r.right[0] for r in lexical_rules.get("V_3SG_ant", [])]

# Create dictionaries for feature building
verb_to_inf        = dict(zip(v_3sg_list,   v_inf_list))         # 3SG -> INF
verb_to_ant_inf    = dict(zip(v_inf_ant_list,  v_inf_neg_list))  # ant-INF -> neg-INF
verb_to_ant_3sg_1  = dict(zip(v_3sg_neg_list, v_inf_neg_list))   # neg-3SG -> neg-INF
verb_to_ant_3sg_2  = dict(zip(v_3sg_ant_list, v_inf_neg_list))   # ant-3SG -> neg-INF

# ----------------------------------------
# Populate the grammars with lexical rules
# ----------------------------------------

# Store populated grammars (will be used to generate examples)
fcp = {}

for name, grammar in fcp_base.items():
    fcp[name] = deepcopy(grammar)

    # Add lexical rules: if grammar has a placeholder symbol that matches keys in lexical_rules,
    # extend the grammar with those lexical rules.
    new_rules = set()
    
    for rule in grammar:
        for category, rules_list in lexical_rules.items():
            if category in rule.right:
                new_rules.update(rules_list)

    for rule in new_rules:
        if rule not in fcp[name]:
            fcp[name].append(rule)

    # Add relevant features
    for rule in fcp[name]:
        if rule.left == "NP":
            rule.features.setdefault("subj", rule.right[0])
        
        if rule.left == "V_INF":
            rule.features.setdefault("verb", rule.right[0])
        if rule.left == "V_3SG":
            rule.features.setdefault("verb", verb_to_inf.get(rule.right[0], rule.right[0]))
        
        if rule.left == "V_INF_neg":
            rule.features.setdefault("verb", rule.right[0])
            rule.features.setdefault("ant", "n")
        if rule.left == "V_INF_ant":
            rule.features.setdefault("verb", verb_to_ant_inf.get(rule.right[0], rule.right[0]))
            rule.features.setdefault("ant", "y")
        
        if rule.left == "V_3SG_neg":
            rule.features.setdefault("verb", verb_to_ant_3sg_1.get(rule.right[0], rule.right[0]))
            rule.features.setdefault("ant", "n")
        if rule.left == "V_3SG_ant":
            rule.features.setdefault("verb", verb_to_ant_3sg_2.get(rule.right[0], rule.right[0]))
            rule.features.setdefault("ant", "y")
