import torch
from collections import defaultdict
from typing import List, Dict, Any, Tuple, Optional


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
    Returns a dictionary mapping each lexical category to a list of token lists (each list corresponding to filled masks) ordered by joint probability.

    -   prompts: A dictionary mapping each lexical category (e.g., 'Verb') to a list of prompts containing <mask>.
    -   tokenizer: The tokenizer used to encode the prompts.
    -   model: The masked language model used to predict replacements for <mask>.
    -   top_k: Number of top predictions to retain globally per category.
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


def format_lexical_pool():
    pass


def format_rules(lexical_pool: Dict[str, List[str]]) -> List[str]:
    """
    Convert a lexical pool into CFG rule strings in the format Rule(left="Category", right=["item"]).
    Returns a list of formatted rule strings ready to be used in a CFG.

    -   lexical_pool: A dictionary of lexical categories to lists of lexical items.
    """

    # List of rules
    rules = []

    # Go over the items in the lexical pool
    for category, items in lexical_pool.items():

        # Iterate over each lexical item for the current category
        for item in items:

            # Format as a Rule CFG string and append to the list
            rules.append(f'Rule(left="{category}", right=["{item}"])')

    return rules
