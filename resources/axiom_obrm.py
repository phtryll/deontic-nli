from source.cfg_utils import Rule

my_rules = [

    # The following rules generate premises and hypothesis as pseudo-formulas
    Rule(left="S", right=["[Premise]", "AFFIRMATION", "."], prob=0.33),
    Rule(left="S", right=["[Hypothesis]", "DEONTIC_AFFIRMATION", "."], prob=0.33),
    Rule(left="S", right=["[Premise]", "COMPOUND_PREMISE", "."], prob=0.34),

    Rule(left="AFFIRMATION", right=["if", "PROP_1", "then", "PROP_2"]), # p implies q
    Rule(left="DEONTIC_AFFIRMATION", right=["if", "MOD_1", "then", "MOD_2"], prob=0.5), # OB(p) implies OB(q)
    Rule(left="DEONTIC_AFFIRMATION", right=["MOD_2"], prob=0.5), # OB(q)
    Rule(left="COMPOUND_PREMISE", right=["AFFIRMATION", ".", "MOD_1"]), # p implies q and OB(p)

    Rule(left="MOD_1", right=["it is obligatory that", "PROP_1"]),
    Rule(left="MOD_2", right=["it is obligatory that", "PROP_2"]),
    Rule(left="PROP_1", right=["p"]),
    Rule(left="PROP_2", right=["q"]),

]