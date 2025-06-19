from source.utils import Rule

operators_natural = [

    # Axiom
    Rule(left="S", right=["F"]),
    Rule(left="S", right=["Modal", "F"]),
    Rule(left="S", right=["(", "F", ")", "si et seulement si", "(", "F", ")"]),
    Rule(left="S", right=["(", "F", ")", "implique", "(", "F", ")"]),

    # Intermediary
    Rule(left="F", right=["Form"]),
    Rule(left="F", right=["Modal", "Form"]),
    Rule(left="F", right=["(", "Form", ")", "et", "(", "Form", ")"]),
    Rule(left="F", right=["(", "Form", ")", "ou", "(", "Form", ")"]),

    # # Formules
    Rule(left="Form", right=["Neg", "Modal", "Arg"]),
    Rule(left="Form", right=["Modal", "Arg"]),
    Rule(left="Form", right=["Arg"]),

    # Modaux
    Rule(left="Modal", right=["il est permis que"]),
    Rule(left="Modal", right=["il est obligatoire que"]),
    Rule(left="Modal", right=["il est interdit que"]),
    Rule(left="Modal", right=["il est optionnel que"]),
    Rule(left="Modal", right=["il est omissible que"]),
    Rule(left="Modal", right=["il est non-optionnel que"]),

    # Arguments
    Rule(left="Arg", right=["p"]),
    Rule(left="Arg", right=["q"]),
    # Rule(left="Arg", right=["non", "p"]),
    # Rule(left="Arg", right=["non", "q"]),

    # Other
    Rule(left="Neg", right=["il n'est pas le cas que"]),


]