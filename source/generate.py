import time
from ollama import chat
from pydantic import create_model, ConfigDict, Field, conlist
from source.cfg import CFG
from source.cfg_utils import join, Rule
from typing import List, Dict, Any
from tqdm import tqdm


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


def generate_items(prompt: str,  k: int, field_names: List[str], model: str = 'mistral') -> Dict[str, List[str]]:
    """
    Generate lexical items for a given prompt, enforcing a strict JSON schema.
    Returns a dict mapping each field name to its list of generated strings.
    """

    # Define the format fields (they correspond to the entry labels, i.e. the non-terminals)
    fields: Any = {name: (conlist(str, min_length=k, max_length=k), Field()) for name in field_names}

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
        f'You are a JSON generator. You must output only valid JSON that conforms exactly to the provided schema. '
        f'You will receive an instruction to “Generate exactly {k} items.” You must return exactly {k} elements in each list. '
    )

    # Prepare the system and user messages for the ollama chat API
    system_msg = {'role': 'system', 'content': system_prompts}
    user_msg = {'role': 'user', 'content': prompt}

    start = time.time()

    # Streaming call
    response = chat(
        messages=[system_msg, user_msg],
        model=model,
        format=json_schema,
        stream=True,
    )

    # Stream tokens and show a live progress indicator
    chunks = []
    with tqdm(total=None, desc="Generating", unit="tok") as pbar:
        for chunk in response:
            token = chunk["message"]["content"]
            chunks.append(token)
            pbar.update(1)

    elapsed = time.time() - start
    print(f"Generation took {elapsed:.2f}s")

    content = "".join(chunks)
    if not content:
        raise ValueError("No content in model response")

    # Validate the JSON response against our schema
    try:
        instance = SchemaClass.model_validate_json(content)
    except Exception as e:
        raise ValueError("Output format was not validated") from e

    # Enforce exact length for each field
    data = instance.model_dump()
    for field, items in data.items():
        if len(items) != k:
            raise ValueError(f"{field}: expected {k} items, got {len(items)}")

    return data


def format_rules(slot_dict: Dict[str, List[str]]) -> Dict[str, List[Rule]]:
    """
    Convert a slot-mapped dict into CFG Rule objects.
    For each slot_label, produce a list of Rule(...) instances.
    Returns: Dict[slot_label, List[Rule]].
    """
    
    # Map each slot label to its list of rule strings
    rules_map: Dict[str, List[Rule]] = {}

    # Iterate over slot labels and their predicted items
    for slot_label, items in slot_dict.items():
        
        # Collect rule strings for this slot_label
        rules: List[Rule] = []
        
        # Create a Rule string for each item
        for item in items:
            rules.append(Rule(left=slot_label, right=[item]))
        
        rules_map[slot_label] = rules

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