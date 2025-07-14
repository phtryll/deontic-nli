import random
from collections import defaultdict
from typing import Set, List, Dict, DefaultDict, Any, Optional
from source.cfg_utils import Rule, Tree, unify


class CFG:
    "Class for the context-free grammar."

    def __init__(self, rules: List[Rule], axiom: str) -> None:
        """
        Initialize the CFG with a list of rules and an axiom (starting non-terminal symbol).
        It collects non-terminals, terminals, and builds mappings from non-terminals to their rules.
        It also normalizes rule probabilities for each non-terminal to sum to 1.0.

        -   rules (List[Rule]): a list of CFG rules.
        -   axiom (str): the starting non-terminal symbol of the grammar.
        -   non_terminals (set): the set of non-terminal symbols N gathered from the left-hand side of the rules.
        -   terminals (set): the set of terminal symbols collected from the right-hand side of rules that are not in non-terminals.
        -   mappings (Dict): a dictionary that maps each non-terminal to its corresponding rules.
        """

        self.rules: List[Rule] = rules
        self.axiom: str = axiom
        self.non_terminals: Set[str] = set(rule.left for rule in self.rules)
        self.terminals: Set[str] = set()
        self.mappings: DefaultDict[str, List[Rule]] = defaultdict(list)

        # Populate the set of terminals
        for rule in self.rules:
            for symbol in rule.right:
                if symbol not in self.non_terminals:
                    self.terminals.add(symbol)

        # Build mappings
        for rule in self.rules:
            self.mappings[rule.left].append(rule)

        # Normalize rule probabilities for each non-terminal to sum to 1.0
        for non_terminal, rules_for_non_terminal in self.mappings.items():
            total_probability = sum(rule.prob for rule in rules_for_non_terminal)

            # If it is not the case: auto-normalize
            if abs(total_probability - 1.0) > 1e-6:
                print(
                    f"[INFO] Normalizing rule probabilities for '{non_terminal}' "
                    f"(sum was {total_probability:.2f})."
                )
                
                # Each possible rule of a non terminal will get same value
                for rule in rules_for_non_terminal:
                    rule.prob /= total_probability

    def is_terminal(self, symbol: str) -> bool:
        """Helper. Checks if a symbol is terminal."""

        return symbol in self.terminals
    
    def is_non_terminal(self, symbol: str) -> bool:
        """Helper. Checks if a symbol is a non terminal."""

        return symbol in self.non_terminals
    
    def is_variable(self, value: Any) -> bool:
        """Check if the feature value is a variable (string starting with '?')."""

        return isinstance(value, str) and value.startswith('?')

    def generate(self, verbose=False):
        """Generate a grammar tree."""

        # Non terminal feature bindings: initialize an empty dict for each non-terminal
        self.feature_bindings: Dict[str, Dict[str, Any]] = {non_terminal: {} for non_terminal in self.mappings}

        # Initialize a tree with the axiom as the starting label
        tree: Tree = Tree(node_label=self.axiom, features={})
        
        # Stack holds tuples of (node, parent_label)
        stack: List[tuple[Tree, Optional[str]]] = [(tree, None)]

        # Main loop: continue until stack is empty
        while stack:

            # Processing the last node from the stack
            node, parent_label = stack.pop()

            # Get the local bindings for this non terminal
            local_bindings = self.feature_bindings.get(node.node_label, {})

            # Check if that node is terminal: if yes skip
            if self.is_terminal(node.node_label):
                continue

            # Assert that the node is a non-terminal or raise error
            assert self.is_non_terminal(node.node_label), (
                f"Unknown symbol: {node.node_label}"
            )

            # Retrieve applicable rules for this non-terminal
            applicable_rules = self.mappings[node.node_label]
            
            # Filter by feature unification
            candidates = []
            for rule in applicable_rules:
                context = {**node.features, **local_bindings}
                # context = node.features
                merged_features = unify(context, rule.features)

                if merged_features is not None:
                    candidates.append((rule, merged_features))
                
            # else:
            assert candidates, f"No applicable rules for {node.node_label} with features {node.features}"

            # Always sample one rule according to weights
            weights = [rule.prob for rule, _ in candidates]
            selected_rule, selected_features = random.choices(candidates, weights=weights, k=1)[0]

            # Record any variable→constant binding in the parent non-terminal
            if parent_label in self.feature_bindings:
                for feature, value in selected_features.items():
                    node_value = node.features.get(feature)
                    rule_value = selected_rule.features.get(feature)
                    if self.is_variable(node_value) or self.is_variable(rule_value):
                        self.feature_bindings[parent_label][feature] = value

            # Create children with current global variable bindings
            node.children = [
                Tree(node_label=symbol, features=selected_features)
                for symbol in selected_rule.right
            ]

            # Push children along with this node as their parent
            for child in reversed(node.children):
                stack.append((child, node.node_label))

            # If verbose: print the current state of the tree
            if verbose:
                print(f"Applied rule: {node.node_label} -> {selected_rule.right}")
                print(f"Current tree: {tree}")
        
        return tree
    
    def __str__(self) -> str:
        """String representation of the rule."""

        # Format nicely the elements of the CFG
        formatted_terminals = "\n   - ".join(str(t) for t in self.terminals)
        formatted_non_terminals = "\n   - ".join(str(nt) for nt in self.non_terminals)
        formatted_rules = "\n   - ".join(str(rule) for rule in self.rules)

        context_free_grammar = (
            "CFG/PCFG: a tuple containing:\n\n"
            f"An axiom:\n   - {self.axiom}\n\n"
            f"A set of terminals:\n   - {formatted_terminals}\n\n"
            f"A set of non-terminals:\n   - {formatted_non_terminals}\n\n"
            f"A set of rules:\n   - {formatted_rules}\n"
        )

        return context_free_grammar
    
    def __repr__(self) -> str:
        """Internal representation. Calls __str__"""

        return self.__str__()
