from source.cfg_utils import Rule

my_rules = [

    # Axiom
    Rule(left="S", right=["MOD_F"]),
    Rule(left="S", right=["(", "MOD_F", ")", "⋀", "(", "MOD_F", ")"]),
    Rule(left="S", right=["(", "MOD_F", ")", "⋁", "(", "MOD_F", ")"]),
    Rule(left="MOD_F", right=["MOD", "FORM"]),
    Rule(left="MOD_F", right=["¬", "MOD", "FORM"]),
    Rule(left="FORM", right=["PROP"]),
    Rule(left="FORM", right=["¬", "PROP"]),
    Rule(left="PROP", right=["p"]),
    Rule(left="MOD", right=["OB"]),
    Rule(left="MOD", right=["PE"]),
    Rule(left="MOD", right=["FO"]),
    Rule(left="MOD", right=["OP"]),
    Rule(left="MOD", right=["OM"]),
    Rule(left="MOD", right=["NO"])

    # Variations lexicales
    # TODO
]