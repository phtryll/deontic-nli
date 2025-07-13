from source.cfg_utils import Rule

fcp = [

    Rule(
        left="S",
        right=["<PREMISE>", "<HYPOTHESIS>"],
    ),

    Rule(
        left="<PREMISE>",
        right=["[P]", "PE", "COMP", "p", "or", "q", "."],
    ),

    Rule(
        left="<HYPOTHESIS>",
        right=["[H]", "PE", "COMP", "p", "and", "PE", "COMP", "q", "."],
    ),

    Rule(
        left="<PREMISE>",
        right=["[P]", "PE", "COMP", "PROP", "."],
    ),

    Rule(
        left="<HYPOTHESIS>",
        right=["[H]", "PE", "COMP", "PROP", "."],
    ),

    Rule(
        left="<HYPOTHESIS>",
        right=["[H]", "PE", "COMP", "p", "or", "q", "."],
    ),

    Rule(
        left="<PREMISE>",
        right=["[P]", "p", "or", "q"],
    ),

    Rule(
        left="<HYPOTHESIS>",
        right=["[H]", "p", "or", "q"],
    ),

    Rule(
        left="<PREMISE>",
        right=["[P]", "p", "and", "q"],
    ),

    Rule(
        left="<HYPOTHESIS>",
        right=["[H]", "p", "and", "q"],
    ),

    Rule(
        left="<HYPOTHESIS>",
        right=["[H]", "PROP"],
    ),

    Rule(
        left="<PREMISE>",
        right=["[P]", "PROP"],
    ),

    Rule(left="PE", right=["it is", "NEG", "permitted"]),
    Rule(left="NEG", right=["not"]),
    Rule(left="NEG", right=[""]),
    
    Rule(left="COMP", right=["that"]),

    Rule(left="PROP", right=["p"]),
    Rule(left="PROP", right=["q"]),
    Rule(left="p", right=["A"]),
    Rule(left="q", right=["B"]),
    
]