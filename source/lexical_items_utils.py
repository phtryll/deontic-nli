import torch
from collections import defaultdict
from typing import List, Dict, Any, Tuple


# Function to get top-k mask completions with probabilities
def fill_mask(prompt: str, tokenizer: Any, model: Any, top_k: int = 50) -> List[Tuple[str, float]]:
    """
    Fill the masked token in a prompt using CamemBERT's masked language modeling.
    Returns the top_k predicted words or phrases and their probabilities.

    -   prompt (str): A sentence with a single <mask> token representing the word to predict.
    -   tokenizer: HuggingFace tokenizer instance for CamemBERT.
    -   model: HuggingFace model instance for masked language modeling.
    -   top_k (int): Number of top predictions to return.
    """

    # Prepare the prompt to be tokenized and fed to the model: ensure that <mask> is encoded correctly
    masked_text = prompt.replace("<mask>", tokenizer.mask_token)

    # Tokenize the prompt and return tensors for PyTorch
    encoded_input = tokenizer(masked_text, return_tensors="pt")

    # Inference mode: compute the model's raw prediction scores (logits) with no gradient tracking
    with torch.no_grad():
        model_output = model(**encoded_input).logits # Shape: [1, sequence_length, vocab_size]

    # Locate the index position of the masked token
    mask_token_index = (encoded_input.input_ids == tokenizer.mask_token_id)[0].nonzero(as_tuple=True)[0]

    # Select the logits corresponding to the masked token position
    mask_token_logits = model_output[0, mask_token_index]  # Shape: [1, vocab_size]

    # Convert logits to probabilities using softmax
    probabilities = torch.softmax(mask_token_logits, dim=-1)

    # Get the top-k most probable tokens and their probabilities
    top_tokens = torch.topk(probabilities, top_k, dim=1)

    # Transform the ids and probabilities as lists
    token_ids = top_tokens.indices[0].tolist()
    top_probabilities = top_tokens.values[0].tolist()

    # Return list of (decoded token, probability) pairs
    return [(tokenizer.decode([tid]).strip(), probability) for tid, probability in zip(token_ids, top_probabilities)]


def generate_lexical_pool(prompts: Dict[str, List[str]], tokenizer: Any, model: Any, top_k: int = 50) -> Dict[str, List[str]]:
    """
    Generate a dictionary of lexical items for each category using masked language modeling.
    Returns a dictionary mapping each lexical category to the top-k highest probability unique predictions.

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
        seen = {}

        # For each prompt in that category, get predictions
        for prompt in examples:

            # Generate and store predictions
            predictions = fill_mask(prompt, tokenizer, model, top_k)
            scored_words.extend(predictions)

        # For each word, retain only the highest-scoring version
        for word, score in scored_words:
            if word not in seen or score > seen[word]:
                seen[word] = score

        # Sort words by descending score and keep only the top_k
        top_items = sorted(seen.items(), key=lambda x: x[1], reverse=True)[:top_k]

        # Store the final list of lexical items for this category
        pool[category] = [word for word, _ in top_items]

    return pool


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
