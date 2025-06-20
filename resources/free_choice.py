from source.cfg_utils import Rule

my_rules = [

    # Free choice en formule
    Rule(left="S", right=["M_DIS", "→", "M_CONJ"]),
    Rule(left="M_DIS", right=["MOD", "CONJ"]),
    Rule(left="M_CONJ", right=["(", "M_PROP1", "⋀", "M_PROP2", ")"]),
    Rule(left="CONJ", right=["(", "PROP1", "⋁", "PROP2", ")"]),
    Rule(left="M_PROP1", right=["MOD", "PROP1"]),
    Rule(left="M_PROP2", right=["MOD", "PROP2"]),
    Rule(left="PROP1", right=["p"]),
    Rule(left="PROP2", right=["q"]),
    Rule(left="MOD", right=["PE"]),

    # Variations lexicales
    # TODO
]