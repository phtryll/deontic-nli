import random
from collections import defaultdict
from typing import Set, List, DefaultDict
from source.utils import Rule, Tree


class CFG:
    "Class for the context-free grammar."

    def __init__(self, rules: List[Rule], axiom: str) -> None:
        """
        Initialize the CFG with a list of rules, a set of non-terminal
        symbols, a set of terminal symbols, an axiom (starting non-terminal symbol) and a dictionary that maps each non-terminal to a list of rules.

        -   rules (List[Rule]): a list of CFG rules.
        -   axiom (str): the starting non-terminal symbol of the grammar.
        -   non_terminals (set): the set of non-terminal symbols N that we 
            gather from the left-hand side of the rules.
        -   terminals (set): the set of terminal symbols collected from the
            right-hand side of rules, and that are not in the set of
            non-terminals.
        -   mappings (Dict): a dictionary that maps each non-terminal to its
            corresponding rules.
        """

        self.rules: List[Rule] = rules
        self.axiom: str = axiom
        self.non_terminals: Set[str] = set(rule.left for rule in rules)
        self.terminals: Set[str] = set()
        self.mappings: DefaultDict[str, List[Rule]] = defaultdict(list)

        # Populate the set of terminals
        for rule in rules:
            for symbol in rule.right:
                if symbol not in self.non_terminals:
                    self.terminals.add(symbol)

        # Build mappings
        for rule in rules:
            self.mappings[rule.left].append(rule)

    def is_terminal(self, symbol: str) -> bool:
        """Helper. Checks if a symbol is terminal."""

        return symbol in self.terminals
    
    def is_non_terminal(self, symbol: str) -> bool:
        """Helper. Checks if a symbol is a non terminal."""

        return symbol in self.non_terminals
    
    def generate(self, verbose=False):
        """Generate a grammar tree."""

        # Initialize a tree with the axiom as the starting label
        tree: Tree = Tree(node_label=self.axiom)

        # Initialize a stack (LIFO) to hold nodes for rewriting
        stack: List[Tree] = [tree]

        # Main loop: continue until stack is empty
        while stack:

            # Processing the last node from the stack
            node = stack.pop()

            # Check if that node is terminal: if yes skip
            if self.is_terminal(node.node_label):
                continue

            # Assert that the node is a non-terminal or raise error
            assert self.is_non_terminal(node.node_label), (
                f"Unknown symbol: {node.node_label}"
            )

            # Select a random rule from that non-terminal node
            rules = self.mappings[node.node_label]
            rule = random.choice(rules)

            # Apply the rule by creating children nodes from the rule's right
            node.children = [Tree(node_label=symbol) for symbol in rule.right]

            # If verbose: print the current state of the tree
            if verbose:
                print(f"Applied rule: {node.node_label} -> {rule.right}")
                print(f"Current tree: {tree}")

            # Add the new children in the stack in reverse order (left to right)
            stack.extend(reversed(node.children))
        
        return tree
    
    def __str__(self) -> str:
        """String representation of the rule."""

        # Format nicely the elements of the CFG
        formatted_terminals = "\n   - ".join(str(t) for t in self.terminals)
        formatted_non_terminals = "\n   - ".join(str(nt) for nt in self.non_terminals)
        formatted_rules = "\n   - ".join(str(rule) for rule in self.rules)

        context_free_grammar = (
            "CFG: a tuple containing:\n\n"
            f"An axiom: {self.axiom}\n"
            f"A set of terminals:\n   - {formatted_terminals}\n"
            f"A set of non-terminals:\n   - {formatted_non_terminals}\n"
            f"A set of rules:\n   - {formatted_rules}\n"
        )

        return context_free_grammar
    
    def __repr__(self) -> str:
        """Internal representation. Calls __str__"""

        return self.__str__()
