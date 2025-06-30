from typing import List


class Rule:
    """Class to represent a CFG rule."""

    def __init__(self, left: str, right: List[str]) -> None:
        """
        Initialize the left and right sides of the rule.

        -   left (str): the left-hand side symbol (non-terminal).
        -   right (List[str]): the right-hand side symbol(s), a list of strings.
        """

        self.left: str = left
        self.right: List[str] = right

    def __str__(self) -> str:
        """String representation of the rule."""
        
        return f"{self.left} -> {self.right}"
    
    def __repr__(self) -> str:
        """Internal representation. Calls __str__"""
        
        return self.__str__()


class Tree:
    """Class to represent a CFG tree."""

    def __init__(self, node_label: str, children: List["Tree"] | None = None) -> None:
        """
        Initialize the tree with a node. Children are optional.
        
        -   node_label (str): the label of the parent node.
        -   children (List[Tree]): a list with the children of the provided node.
        """

        # If children are not provided, initialize an empty list
        if children is None:
            children = []

        self.node_label: str = node_label
        self.children: List[Tree] = children

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
