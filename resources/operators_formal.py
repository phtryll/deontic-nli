from source.utils import Rule

operators_formal = [

    # Axiom
    Rule(left="S", right=["F"]),
    Rule(left="S", right=["Modal", "F"]),
    Rule(left="S", right=["(", "F", ")", "↔", "(", "F", ")"]),
    Rule(left="S", right=["(", "F", ")", "→", "(", "F", ")"]),

    # Intermediary
    Rule(left="F", right=["Form"]),
    Rule(left="F", right=["Modal", "Form"]),
    Rule(left="F", right=["(", "Form", ")", "∧", "(", "Form", ")"]),
    Rule(left="F", right=["(", "Form", ")", "∨", "(", "Form", ")"]),

    # # Formules
    Rule(left="Form", right=["¬", "Modal", "Arg"]),
    Rule(left="Form", right=["Modal", "Arg"]),
    Rule(left="Form", right=["Arg"]),

    # Modals
    Rule(left="Modal", right=["PE"]),
    Rule(left="Modal", right=["OB"]),
    Rule(left="Modal", right=["FO"]),
    Rule(left="Modal", right=["OP"]),
    Rule(left="Modal", right=["OM"]),
    Rule(left="Modal", right=["NO"]),

    # Arguments
    Rule(left="Arg", right=["p"]),
    Rule(left="Arg", right=["q"]),
    Rule(left="Arg", right=["¬", "p"]),
    Rule(left="Arg", right=["¬", "q"]),
]