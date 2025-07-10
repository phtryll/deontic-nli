import json
import torch
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any, Tuple


def fill_mask(prompt: str, tokenizer: Any, model: Any, top_k: int = 50) -> List[Tuple[List[str], float]]:
    """
    Fill the masked tokens in a prompt sequentially.
    If there is one <mask>, return a list of ([token], probability) for the top_k tokens.
    If there are multiple <mask> tokens, it:
      1. Fills the first mask with each of the top_k candidates.
      2. For each candidate, fills the next mask by selecting its single highest-scoring token in context.
      3. Repeats until all masks are filled.
    Returns a list of tuples (token_list, joint_probability), where token_list length equals number of masks.

    -   prompt (str): Sentence containing one or more <mask> tokens.
    -   tokenizer: HuggingFace tokenizer for a masked LLM.
    -   model: HuggingFace masked language model.
    -   top_k (int): Number of top candidates for the first mask and number of joint results returned.
    """

    # Determine computing device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Move model to the selected device
    model.to(device)

    # Count the number of <mask> tokens in the prompt
    num_masks = prompt.count("<mask>")

    # Tokenize the original prompt
    encoded_input_pre = tokenizer(prompt, return_tensors="pt")

    # Move input tensors to the device
    encoded_input = {key: value.to(device) for key, value in encoded_input_pre.items()}

    # Disable gradient computation for inference
    with torch.no_grad():

        # Run model and get raw logits
        model_output = model(**encoded_input).logits

    # Locate all mask positions
    mask_positions = (encoded_input["input_ids"] == tokenizer.mask_token_id)[0].nonzero(as_tuple=True)[0]

    # Use the first mask position
    mask_pos = mask_positions[0]

    # Extract logits for the first mask
    mask_logits = model_output[0, mask_pos]

    # Convert logits to probabilities
    mask_probs = torch.softmax(mask_logits, dim=-1)

    # Select top_k token candidates
    top_probs, top_indices = torch.topk(mask_probs, top_k)

    # Initialize results list
    results: List[Tuple[List[str], float]] = []

    for prob, idx in zip(top_probs.tolist(), top_indices.tolist()):
        # Decode token ID to string
        token_str = tokenizer.decode([idx]).strip()

        # Append first-mask candidate and its probability
        results.append(([token_str], prob))

    # Sequentially fill remaining masks by selecting best token in context
    for _ in range(1, num_masks):
        # Prepare new results for next mask
        new_results: List[Tuple[List[str], float]] = []

        for tokens_list, score in results:
            # Reset prompt for incremental filling
            masked_text = prompt

            # Insert each already filled token
            for token in tokens_list:
                # Replace one mask at a time
                masked_text = masked_text.replace("<mask>", token, 1)

            # Tokenize updated prompt
            encoded_input_pre2 = tokenizer(masked_text, return_tensors="pt")

            # Move new tensors to device
            encoded_input2 = {key: value.to(device) for key, value in encoded_input_pre2.items()}

            # Inference for updated prompt
            with torch.no_grad():

                # Get logits for the updated prompt
                model_output2 = model(**encoded_input2).logits

            # Locate next mask position
            mask_positions2 = (encoded_input2["input_ids"] == tokenizer.mask_token_id)[0].nonzero(as_tuple=True)[0]

            # Select the next mask index
            mask_pos2 = mask_positions2[0]

            # Extract logits for this mask
            mask_logits2 = model_output2[0, mask_pos2]

            # Compute probabilities
            mask_probs2 = torch.softmax(mask_logits2, dim=-1)

            # Choose best candidate
            top_prob, top_index = torch.topk(mask_probs2, 1)

            # Decode the best token
            next_token = tokenizer.decode([top_index.tolist()[0]]).strip()

            # Get its probability
            next_prob = top_prob.tolist()[0]

            # Append extended fill and updated score
            new_results.append((tokens_list + [next_token], score * next_prob))

        # Update results for subsequent masks
        results = new_results

    # Return all filled token lists and their joint scores
    return results


def generate_lexical_pool(prompts: Dict[str, List[str]], tokenizer: Any, model: Any, top_k: int = 50) -> Dict[str, List[List[str]]]:
    """
    Generate a lexical pool for each category by filling masks in provided prompts.
    For each category:
      1. Call fill_mask on each prompt to get joint predictions.
      2. Deduplicate by keeping only the highest joint-scoring fills.
      3. Sort and select the top_k candidate token lists.
    Returns a dictionary mapping each category to its list of token lists, ordered by joint probability.

    -   prompts (Dict[str, List[str]]): Map from category names to lists of mask-containing prompts.
    -   tokenizer (Any): HuggingFace tokenizer for a masked LLM.
    -   model (Any): HuggingFace masked language model instance.
    -   top_k (int): Number of top joint candidates to retain per category.
    """

    # Dictionary to hold lexical items per category (with insertion order)
    pool = defaultdict(list)

    # For each category (e.g., 'Verb', 'Name') and its associated prompts
    for category, examples in prompts.items():
        
        # Store predicted words
        scored_words = []
        
        # Map from filled-token tuples to their highest joint score
        seen: Dict[Tuple[str, ...], float] = {}

        # For each prompt in that category, get predictions
        for prompt in examples:

            # Generate and store predictions
            predictions = fill_mask(prompt, tokenizer, model, top_k)
            scored_words.extend(predictions)

        # For each word, retain only the highest-scoring version
        for word_list, score in scored_words:
            key = tuple(word_list)
            if key not in seen or score > seen[key]:
                seen[key] = score

        # Sort words by descending score and keep only the top_k
        top_items = sorted(seen.items(), key=lambda x: x[1], reverse=True)[:top_k]

        # Store the final list of lexical items for this category
        pool[category] = [list(key) for key, _ in top_items]

    return pool


def format_lexical_pool(lexical_pool: Dict[str, List[List[str]]], slot_labels_map: Dict[str, List[str]]) -> Dict[str, Dict[str, List[str]]]:
    """
    Format a lexical pool into a mapping from category keys to slot-mapped dictionaries.
    Each category maps to a dict of slot_label → list of predicted tokens.
    Returns: Dict[category, Dict[slot_label, List[str]]].

    - lexical_pool: Map from category to list of token-list predictions.
    - slot_labels_map: Map from category to its corresponding slot label list.
    """

    # Initialize dict to hold formatted output per category
    formatted: Dict[str, Dict[str, List[str]]] = {}

    # Iterate over each category and its fills in the lexical pool
    for category, fills in lexical_pool.items():
        
        # Get slot labels for this category
        labels = slot_labels_map[category]
        
        # Initialize empty list for each slot label
        slot_dict: Dict[str, List[str]] = { label: [] for label in labels }
        
        # Iterate over each fill (list of tokens)
        for fill in fills:
            
            # Assign each token in fill to its corresponding slot label
            for i, label in enumerate(labels):
                slot_dict[label].append(fill[i])
        
        # Map the category to its filled slot dictionary
        formatted[category] = slot_dict
    
    # Return the mapping from category to slot_dict
    return formatted


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


def save_rules(structured_rules: Dict[str, Dict[str, List[str]]]) -> None:
    """
    Save a nested mapping of category→slot_label→rule strings to data/lexical_rules_pool.json.
    If the file exists, load the existing structure and merge new entries (deduplicating).
    """
    
    # Determine fixed rules file path
    rules_file_path = Path.cwd() / "data" / "lexical_rules_pool.json"
    
    # Ensure directory exists
    rules_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing rules map if file exists
    if rules_file_path.exists():
        with open(rules_file_path, 'r', encoding='utf-8') as file:
            existing_rules_map = json.load(file)
    
    # No existing file: start with an empty rules map
    else:
        existing_rules_map: Dict[str, Dict[str, List[str]]] = {}
    
    # Merge new structured rules
    for category, slot_map in structured_rules.items():
        if category not in existing_rules_map:
            existing_rules_map[category] = {}
        
        # For each slot label under this category
        for slot_label, rule_list in slot_map.items():

            # Merge with existing rule list and remove duplicates
            if slot_label in existing_rules_map[category]:
                
                # Append and dedupe, preserving order
                combined = existing_rules_map[category][slot_label] + rule_list
                seen = set()
                deduped = []
                for rule in combined:
                    if rule not in seen:
                        seen.add(rule)
                        deduped.append(rule)
                existing_rules_map[category][slot_label] = deduped
            
            else:
                existing_rules_map[category][slot_label] = rule_list
    
    # Write merged rules map to JSON
    with open(rules_file_path, 'w', encoding='utf-8') as file:
        json.dump(existing_rules_map, file, ensure_ascii=False, indent=4)


def save_lexical_pool(lexical_pool: Dict[str, List[List[str]]]) -> None:
    """
    Save lexical_pool dict by merging into root/data/lexical_items_pool.json.
    If the file exists, load existing dict and append new items per category.
    """
    
    # Use current working directory as project root for the data folder
    file_path = Path.cwd() / "data" / "lexical_items_pool.json"
    
    # Ensure directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing pool if file exists
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_pool = json.load(f)
    else:
        existing_pool = {}
    
    # Merge new items
    for category, items in lexical_pool.items():
        if category in existing_pool:
            existing_pool[category] += items
        else:
            existing_pool[category] = items

    # Deduplicate items per category, preserving order
    for category, items in existing_pool.items():
        seen = set()
        deduped = []
        for entry in items:
            key = tuple(entry)
            if key not in seen:
                seen.add(key)
                deduped.append(entry)
        existing_pool[category] = deduped

    # Write JSON
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_pool, f, ensure_ascii=False, indent=4)


def save_examples(examples: Dict[str, List[str]]) -> None:
    """
    Save generated examples by merging into data/examples.json.
    If the file exists, load existing data and append new examples per grammar.
    """
    
    # Use current working directory as project root for the data folder
    file_path = Path.cwd() / "data" / "examples.json"

    # Ensure directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing examples if present
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_examples = json.load(f)
    else:
        existing_examples = {}

    # Merge new examples
    for grammar_name, new_list in examples.items():
        if grammar_name in existing_examples:
            existing_examples[grammar_name] += new_list
        else:
            existing_examples[grammar_name] = new_list

    # Deduplicate, preserving order
    for grammar_name, example_list in existing_examples.items():
        seen = set()
        deduped = []
        for example in example_list:
            if example not in seen:
                seen.add(example)
                deduped.append(example)
        existing_examples[grammar_name] = deduped

    # Write to JSON
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_examples, f, ensure_ascii=False, indent=4)
