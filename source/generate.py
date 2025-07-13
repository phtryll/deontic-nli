import json
from ollama import chat
from pydantic import RootModel
from source.cfg import CFG
from source.cfg_utils import join
from typing import List, Dict


def generate_examples(grammar: CFG, num_examples: int = 20, print_tree: bool = False) -> List[str]:
    """Generates examples produced by a grammar."""

    examples: List[str] = []

    # Generate examples
    for _ in range(num_examples):

        # Generate a random tree
        tree = grammar.generate(False)

        # Get the terminal yield of the tree
        tokens = tree.output()

        # See the tree structure and the yield
        if print_tree:
            print("sampled tree:", tree) # Print the tree structure
            print("yield:", tokens) # Print the yield (list of tokens)
        
        example = join(tokens) # Join the tokens into a sentence
        examples.append(example) # Add it to the list
    
    return examples


class LexicalPoolSchema(RootModel[List[str]]):
    """Root model for a mapping from category to list of generated items."""
    pass


def generate_with_ollama(prompt: str, model: str = 'mistral') -> List[str]:
    """
    Generate lexical items for each category using ollama.
    Returns: dict mapping category to list of items.

    - prompt: a prompt string.
    - model: ollama model name.
    """
    
    system_msg = {
        'role': 'system',
        'content': (
            'You are a helpful assistant that generates lexical items. '
            'You follow the exact instructions of the prompt. '
        
        )
    }

    user_msg = {
        'role': 'user',
        'content': prompt
    }

    response = chat(
        messages=[system_msg, user_msg],
        model=model,
        format=LexicalPoolSchema.model_json_schema(),
    )

    content = response.message.content
    if content is None:
        raise ValueError("No content in model response")
    
    # Validate and parse JSON to dict
    lexical_pool = LexicalPoolSchema.model_validate_json(content).root
    
    return lexical_pool


def format_rules(slot_dict: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Convert a slot-mapped dict into CFG rule strings.
    For each slot_label, produce a list of Rule(...) strings.
    Returns: Dict[slot_label, List[rule_str]].
    """
    
    # Map each slot label to its list of rule strings
    rules_map: Dict[str, List[str]] = {}

    # Iterate over slot labels and their predicted items
    for slot_label, items in slot_dict.items():
        
        # Collect rule strings for this slot_label
        rule_strs: List[str] = []
        
        # Create a Rule string for each item
        for item in items:
            rule_strs.append(f'Rule(left="{slot_label}", right=["{item}"])')
        
        rules_map[slot_label] = rule_strs

    # Return the mapping of slot labels to rule string lists
    return rules_map


def format_examples(input: Dict[str, List[str]]) -> Dict[str, List[tuple[str, str]]]:
    """Format examples as premise/hypothesis tuples."""

    formatted_examples: Dict[str, List[tuple[str, str]]] = {}

    for grammar, examples in input.items():
        formatted_examples[grammar] = []

        for example in examples:
            if "[H]" in example:
                premise, hypothesis = example.split("[H]", 1)
                premise = premise.replace("[P]", "", 1).strip()
                hypothesis = hypothesis.strip()
                formatted_examples[grammar].append((premise, hypothesis))
    
    return formatted_examples