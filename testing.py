from source.generate import generate_examples
from source.cfg import CFG
from resources.operators_formal import operators_formal
from resources.operators_natural import operators_natural

# Initialize grammar
grammar = CFG(rules=operators_natural, axiom="S")
print("\n----Context-free grammar----\n")
print(grammar)
print("----Generated examples----\n")
generate_examples(grammar, 5, print_tree=False)
print()
