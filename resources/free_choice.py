import os
import json
from source.cfg_utils import Rule

fcp_base = [

    # -------------------
    # p ou q implique p/q
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "PROP", "."]),

    Rule(left="PROP", right=["A"]),
    Rule(left="PROP", right=["B"]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a'}),
    Rule(left="B", right=["V_3SG"], features={'verb':'?b'}),

    # ----------------------
    # p ou q implique p et q
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "A", "and", "B", "."]),

    Rule(left="PROP", right=["A"]),
    Rule(left="PROP", right=["B"]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a'}),
    Rule(left="B", right=["V_3SG"], features={'verb':'?b'}),

    # -----------------------
    # p and q implique p or q
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "A", "and", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "A", "or", "B", "."]),

    Rule(left="PROP", right=["A"]),
    Rule(left="PROP", right=["B"]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a'}),
    Rule(left="B", right=["V_3SG"], features={'verb':'?b'}),

    # -------------------
    # p/q implique p ou q
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "PROP", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "A", "or", "B", "."]),

    Rule(left="PROP", right=["A"]),
    Rule(left="PROP", right=["B"]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a'}),
    Rule(left="B", right=["V_3SG"], features={'verb':'?b'}),

    # ---------------------------------
    # PE (p or q) implies PE p and PE q
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "and", "is permitted to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),

    # ---------------------------------
    # PE (p or q) implies PE p or PE q
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "or", "is permitted to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),

    # ---------------------------------
    # PE (p and q) implies PE p and PE q
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "and", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "and", "is permitted to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),

    # -----------------------------
    # PE_p_or_q_implies_PE_p_/_PE_q
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "PROP", "."]),

    Rule(left="PROP", right=["A"]),
    Rule(left="PROP", right=["B"]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),

    # ---------------------------------
    # PE (p or q) implies PE p and q
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "and", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),

    # -----------------------------
    # PE p or PE q implies PE (p or q)
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "is permitted to", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),

    # -----------------------------
    # PE p and PE q implies PE (p and q)
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "and", "is permitted to", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "and", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),

    # ------------------------------------------------------
    # PE_p_or_q_implies_non_PE_p_and_PE_q_négation_explicite
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["NEG", "SUBJ", "is permitted to", "A", "and", "is permitted to", "B", "."]),

    Rule(left="NEG", right=["it is not the case that"]),
    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),

    # ---------------------------------------------------------
    # PE_p_or_q_implies_non_PE_p_/_non_PE_q_négation_explicite
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["NEG", "SUBJ", "is permitted to", "PROP", "."]),

    Rule(left="PROP", right=["A"]),
    Rule(left="PROP", right=["B"]),

    Rule(left="NEG", right=["it is not the case that"]),
    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),

    # ------------------------------------------------------
    # PE_p_or_q_implies_non_PE_p_and_PE_q_négation_implicite
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

    # --------------------------------------------------------
    # PE_p_or_q_implies_non_PE_p_/_non_PE_q_négation_implicite
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

    # ---------------------------------------------------------
    # p_implies_not_the_case_that_p_explicit
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "A", "."]),
    Rule(left="<HYPOTHESIS>", right=["NEG", "SUBJ", "A", "."]),

    Rule(left="NEG", right=["it is not the case that"]),
    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a'}),

    # ---------------------------------------------------------
    # p_implies_doesn't_p_explicit
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "XA", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "NEG", "YA", "."]),

    Rule(left="NEG", right=["doesn't"]),
    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="XA", right=["A"], features={'p':'y'}),
    Rule(left="YA", right=["A"], features={'p':'n'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a', 'p':'y'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a', 'p':'n'}),

    # ---------------------------------------------------------
    # p_implies_not_the_case_that_q_explicit
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "A", "."]),
    Rule(left="<HYPOTHESIS>", right=["NEG", "SUBJ", "B", "."]),

    Rule(left="NEG", right=["it is not the case that"]),
    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a'}),
    Rule(left="B", right=["V_3SG"], features={'verb':'?a'}),

    # ---------------------------------------------------------
    # p_implies_doesn't_q_explicit
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "A", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "NEG", "B", "."]),

    Rule(left="NEG", right=["doesn't"]),
    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_3SG"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?a'}),

    # ---------------------------------------------------------
    # p_implies_not_p_implicit
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "XA", "."]),
    Rule(left="<HYPOTHESIS>", right=["NEG", "SUBJ", "YA", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="NEG", right=["it is not the case that"]),

    Rule(left="XA", right=["A"], features={'ant':'n'}),
    Rule(left="YA", right=["A"], features={'ant':'y'}),

    Rule(left="A", right=["V_3SG_neg"], features={'verb':'?a', 'ant':'n'}),
    Rule(left="A", right=["V_3SG_ant"], features={'verb':'?a', 'ant':'y'}),

    # ---------------------------------------------------------
    # p_implies_doesn't_p_implicit
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "XA", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "NEG", "YA", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="NEG", right=["doesn't"]),

    Rule(left="XA", right=["A"], features={'ant':'n'}),
    Rule(left="YA", right=["A"], features={'ant':'y'}),

    Rule(left="A", right=["V_3SG_neg"], features={'verb':'?a', 'ant':'n'}),
    Rule(left="A", right=["V_INF_ant"], features={'verb':'?a', 'ant':'y'}),

    # ---------------------------------
    # PE_p_or_q_implies_PE_p_and_FO_q
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "and", "is forbidden to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),

    # ---------------------------------
    # PE_p_or_q_implies_FO_p_and_PE_q
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is forbidden to", "A", "and", "is permitted to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),

    # ---------------------------------
    # PE_p_or_q_implies_FO_p_or_FO_q
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "or", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is forbidden to", "A", "or", "is forbidden to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),

    # ---------------------------------
    # PE_p_and_q_implies_PE_p_or_FO_q
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "and", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is permitted to", "A", "or", "is forbidden to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),

    # ---------------------------------
    # PE_p_and_q_implies_FO_p_or_PE_q
    Rule(left="S", right=["[P]", "<PREMISE>", "[H]", "<HYPOTHESIS>"]),

    Rule(left="<PREMISE>", right=["SUBJ", "is permitted to", "A", "and", "B", "."]),
    Rule(left="<HYPOTHESIS>", right=["SUBJ", "is forbidden to", "A", "or", "is permitted to", "B", "."]),

    Rule(left="SUBJ", right=["NP"], features={'subj':'?x'}),
    Rule(left="A", right=["V_INF"], features={'verb':'?a'}),
    Rule(left="B", right=["V_INF"], features={'verb':'?b'}),

]

fcp = list(fcp_base)
seen_rules = set()

# Load lexical item grammar rules
rule_files = [
    "rules_NP.json",
    "rules_VP.json",
    "rules_VP_NEG.json"
]

# Verb cell matching
v_inf_list = []
v_3sg_list = []
V_INF_neg_list = []
V_INF_ant_list = []
V_3sg_neg_list = []
V_3sg_ant_list = []

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

    if "V_INF" in rules and "V_3SG" in rules:
        v_inf_list = [eval(entry).right[0] for entry in rules["V_INF"]]
        v_3sg_list = [eval(entry).right[0] for entry in rules["V_3SG"]]

    if "V_INF_neg" in rules and "V_INF_ant" in rules:
        V_INF_neg_list = [eval(entry).right[0] for entry in rules["V_INF_neg"]]
        V_INF_ant_list = [eval(entry).right[0] for entry in rules["V_INF_ant"]]
    
    if "V_3SG_neg" in rules and "V_3SG_ant" in rules:
        V_3sg_neg_list = [eval(entry).right[0] for entry in rules["V_3SG_neg"]]
        V_3sg_ant_list = [eval(entry).right[0] for entry in rules["V_3SG_ant"]]

verb_to_inf      = dict(zip(v_3sg_list,   v_inf_list))
verb_to_ant_inf  = dict(zip(V_INF_ant_list,  V_INF_neg_list))
verb_to_ant_3sg_1  = dict(zip(V_3sg_neg_list, V_INF_neg_list))
verb_to_ant_3sg_2  = dict(zip(V_3sg_ant_list, V_INF_neg_list))

# Add relevant features
for rule in fcp:
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
