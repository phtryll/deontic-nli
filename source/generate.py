from ollama import chat, generate
from pydantic import create_model, ConfigDict, Field
from source.cfg import CFG
from source.cfg_utils import join
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
        examples.append(example) # Add it to the list
    
    return examples


def generate_items(prompt: str, field_names: List[str], model: str = 'mistral') -> Dict[str, List[str]]:
    """
    Generate lexical items for a given prompt, enforcing a strict JSON schema.
    Returns a dict mapping each field name to its list of generated strings.
    """
    
    # Define the format fields (they correspond to the entry labels, i.e. the non-terminals)
    fields: Any = {name: (List[str], Field()) for name in field_names}
    
    # Dynamically create a JSON schema for each prompt
    SchemaClass = create_model(
        "LexicalPoolSchema",
        __config__=ConfigDict(extra='forbid'),
       **fields
    )

    # Extract the JSON Schema from the dynamic model and explicitly forbid additional properties
    json_schema = SchemaClass.model_json_schema()
    json_schema["additionalProperties"] = False

    # System general prompt
    system_prompts = (
        'You are a JSON generator. You must output _only_ valid JSON that conforms exactly to the provided schema. '
        'You will receive an instruction to “Generate exactly {k} items.” You must return exactly {k} elements in each list—no more, no fewer. '
    )

    # Prepare the system and user messages for the ollama chat API
    system_msg = {'role': 'system', 'content': system_prompts}
    user_msg = {'role': 'user', 'content': prompt}

    # Invoke the LLM and instruct it to format output according to our JSON schema
    response = chat(
        messages=[system_msg, user_msg],
        model=model,
        format=json_schema,
        # options={'temperature':0.0} # No surprises...
    )

    # Extract the content (and make sure it exists)
    content = response.message.content
    if content is None:
        raise ValueError("No content in model response")

    # Validate the JSON response against our schema
    try:
        instance = SchemaClass.model_validate_json(content)
    except Exception:
        raise ValueError("Output format was not validated")

    # Return the validated data as a dict
    return instance.model_dump()


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