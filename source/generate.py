from source.cfg import CFG
from source.cfg_utils import join
from source.generate_utils import *
from typing import List, Dict, Any

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
        examples.append(example)
    
    return examples


def generate_rules(prompts: Dict[str, List[str]], tokenizer: Any, model: Any, top_k: int, labels: Dict[str, List[str]]) -> Dict[str, Dict[str, List[str]]]:
    """
    Generate a nested mapping of category → slot_label → rule strings for lexical diversity.
    Uses generate_lexical_pool and format_lexical_pool to handle multi-mask slots.
    
    -   prompts (Dict[str, List[str]]): Map from category names to lists of mask-containing prompts.
    -   tokenizer (Any): HuggingFace tokenizer for a masked LLM.
    -   model (Any): HuggingFace masked language model instance.
    -   top_k (int): Number of top joint candidates to retain per category.
    -   labels (Dict[str, List[str]]): Map from category names to their slot-label lists.
    """
    
    # Generate lexical items pool
    pool = generate_lexical_pool(prompts, tokenizer, model, top_k=top_k)
    
    # Format the lexical pool into a mapping category → slot_dict
    formatted_pools = format_lexical_pool(pool, labels)
    
    # Build nested mapping category → slot_label → list of rule strings
    structured_rules: Dict[str, Dict[str, List[str]]] = {}
    
    for category, slot_dict in formatted_pools.items():
        
        # Format rules for each slot dictionary
        rules_map = format_rules(slot_dict)
        structured_rules[category] = rules_map
    
    # Return the nested category → slot_label → rules mapping
    return structured_rules
