from source.cfg_utils import Rule

my_rules = [

    # OB-RM en formule
    Rule(left="S", right=["(", "FORM", ")", "→", "(", "MOD_FORM", ")"]),
    Rule(left="FORM", right=["PROP1", "→", "PROP2"]),
    Rule(left="MOD_FORM", right=["M_PROP1", "→", "M_PROP2"]),
    Rule(left="M_PROP1", right=["MOD", "PROP1"]),
    Rule(left="M_PROP2", right=["MOD", "PROP2"]),
    Rule(left="PROP1", right=["p"]),
    Rule(left="PROP2", right=["q"]),
    Rule(left="MOD", right=["OB"]),

    # Variations lexicales avec deux ensembles A et B ou B incus dans A
    # TODO
]