from typing import List, Dict, Any, Optional


class Rule:
    """Class to represent a CFG rule."""

    def __init__(self, left: str, right: List[str], prob: float = 1.0, features: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the left and right sides of the rule.

        -   left (str): the left-hand side symbol (non-terminal).
        -   right (List[str]): the right-hand side symbol(s), a list of strings.
        -   prob (float): the probability of the rule (default 1.0).
        -   features (Optional[Dict[str, Any]]): optional feature bundle for the rule.
        """

        self.left: str = left
        self.right: List[str] = right
        self.prob: float = prob
        self.features: Dict[str, Any] = features or {}

    def __str__(self) -> str:
        """String representation of the rule, showing probability and features when present."""

        # Simple CFG rule
        base = f"{self.left} -> {' '.join(self.right)}"
        parts = [base]
        
        # Include optional probability
        if self.prob != 1.0:
            parts.append(f"[probability: {self.prob:.3f}]")
        
        # Include optional features
        if self.features:
            rule_features = ", ".join(f"{key}={value}" for key, value in self.features.items())
            parts.append(f"[features: {rule_features}]")
        
        return " ".join(parts)
    
    def __repr__(self) -> str:
        """Internal representation. Calls __str__"""
        
        return self.__str__()

    def __eq__(self, other) -> bool:
        """Equality based on left-hand side and right-hand side symbols."""

        if not isinstance(other, Rule):
            return NotImplemented
        
        return (self.left, tuple(self.right)) == (other.left, tuple(other.right))

    def __hash__(self) -> int:
        """Hash based on left-hand side and right-hand side symbols."""
        
        return hash((self.left, tuple(self.right)))


class Tree:
    """Class to represent a CFG tree."""

    def __init__(self, node_label: str, children: List["Tree"] | None = None, features: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the tree with a node. Children are optional.
        
        -   node_label (str): the label of the parent node.
        -   children (List[Tree]): a list with the children of the provided node.
        -   features (Optional[Dict[str, Any]]): optional feature bundle for the tree node.
        """

        # If children are not provided, initialize an empty list
        if children is None:
            children = []

        self.node_label: str = node_label
        self.children: List[Tree] = children
        self.features: Dict[str, Any] = features or {}

    def output(self) -> List[str]:
        """Iteratively get the output of the tree as a sequence of terminal symbols."""

        # Initialize empty list to store the terminal symbols and a stack
        tree_output: List[str] = []
        stack: List[Tree] = [self]

        while stack:
            node = stack.pop()

            # If the corresponding node is a leaf (no children)
            if not node.children:
                tree_output.append(node.node_label)
            
            # Else, reverse children to process them left to right
            else:
                stack.extend(reversed(node.children))
        
        return tree_output
    
    def __str__(self) -> str:
        """Return a string representation of the tree in bracketed notation."""

        # Initialize an empty list and a stack
        tree_output: List[str] = []
        stack: List[tuple[Tree, int]] = [(self, 0)] # (node, visited?)
        
        while stack:
            node, state = stack.pop()
            
            # If the node is a leaf, append it to the tree output
            if not node.children:
                tree_output.append(node.node_label)
            
            # If the node has children ad is visited for the first time
            elif state == 0:

                # Begin non-terminal:
                tree_output.append("[") # Add "["
                tree_output.append(node.node_label) # Add "node_label"
                stack.append((node, 1)) # Push this node again and mark as visited
                
                # Push its children in reverse order to process left to right
                for child in reversed(node.children):
                    stack.append((child, 0))
            
            # If the node has children but is visited, add closing bracket
            else:
                tree_output.append("]")
        
        # Return the tree as a space separated string
        return " ".join(tree_output)


def join(tokens: List[str]) -> str:
    "Function to join a list of tokens into a single string."

    # Initialize list
    list = []
    capitalize_next = False

    # Go over the tokens in the list
    for i, token in enumerate(tokens):
        
        # Skip empty tokens
        if token == "": continue

        # Capitalize first character after punctuation
        if capitalize_next and token:
            token = token[0].upper() + token[1:]
            capitalize_next = False
    
        # Specific punctuation tokens need a space before them
        if i > 0 and token[0] not in {".", "?", ",", ":", " "}:
            list.append(" ")
        
        # Otherwise just append the token
        list.append(token)

        # If this token ends with punctuation, capitalize the next token
        if token and token[-1] in {".", "?", "!", ":", "]"}:
            capitalize_next = True
    
    # Join the elements of the list
    return "".join(list)


def unify(node_features: Dict[str, Any], rule_features: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Merge two feature dicts if compatible, binding variables.
    Returns the merged dict or None on conflict.
    """

    # Initialize the merged dict
    merged: Dict[str, Any] = {}
    
    # For each key, compare values between node and rule:
    for key in set(node_features) | set(rule_features):

        # Get the values (if empty it yields 'None')
        v_node = node_features.get(key)
        v_rule = rule_features.get(key)

        # If node is empty return rule value
        if v_node is None:
            merged[key] = v_rule
        
        # If rule is empty return node value
        elif v_rule is None:
            merged[key] = v_node
        
        # If both have the same value: consistent
        elif v_node == v_rule:
            merged[key] = v_node
        
        # Check variable value consistency
        elif isinstance(v_node, str) and v_node.startswith("?") and isinstance(v_rule, str) and v_rule.startswith("?"):
            raise ValueError(f"Inconsistent variable values for feature '{key}': {v_node} vs {v_rule}")

        # If rule value is a variable: bind it to the node
        elif isinstance(v_rule, str) and v_rule.startswith("?"):
            merged[key] = v_node

        # If node value is a variable: bind it to the rule
        elif isinstance(v_node, str) and v_node.startswith("?"):
            merged[key] = v_rule
        
        # Conflict between two distinct constants
        else:
            return None
    
    return merged