import logging
from transformers import AutoTokenizer, AutoModelForMaskedLM
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

from source.generate_utils import fill_mask, generate_lexical_pool, format_lexical_pool
from source.generate import generate_rules

# Shared tokenizer and model for all tests
tokenizer = AutoTokenizer.from_pretrained("FacebookAI/xlm-roberta-large")
model = AutoModelForMaskedLM.from_pretrained("FacebookAI/xlm-roberta-large")

# Common prompts for location tests
LOCATION_PROMPTS = {
    "LOCATIONS": [
        "The city of <mask> is in the country of <mask>.",
        "We went to <mask>, and visited the little town of <mask>. It was beautiful!"
    ]
}

# Slot labels corresponding to LOCATION_PROMPTS
LOCATION_SLOT_LABELS = {
    "LOCATIONS": ["CITY", "COUNTRY"]
}

def test_fill_mask():
    prompt = "The city of <mask> is in the country of <mask>."
    print("Testing fill_mask on:", prompt)
    beams = fill_mask(prompt, tokenizer, model, top_k=20)
    for i, (tokens, score) in enumerate(beams, 1):
        print(f"  Beam {i}: {tokens}  (joint score={score:.5f})")
    print()

def test_generate_lexical_pool():
    prompts = LOCATION_PROMPTS

    print("Testing generate_lexical_pool...")
    pool = generate_lexical_pool(prompts, tokenizer, model, top_k=10)
    for category, items in pool.items():
        print(f"{category}:")
        for item in items:
            print("  ", item)
    print()


def test_format_lexical_pool():
    prompts = LOCATION_PROMPTS

    # Generate and then format the lexical pool
    pool = generate_lexical_pool(prompts, tokenizer, model, top_k=10)
    slot_labels_map = LOCATION_SLOT_LABELS
    formatted = format_lexical_pool(pool, slot_labels_map)

    print("Testing format_lexical_pool...")
    for slot_dict in formatted:
        print(slot_dict)
    print()

def test_generate_rules():
    prompts = LOCATION_PROMPTS

    print("Testing generate_rules...")
    generate_rules(prompts, tokenizer, model, top_k=10, labels=LOCATION_SLOT_LABELS)
    print()

def main():
    print("=== fill_mask test ===")
    test_fill_mask()

    print("=== generate_lexical_pool test ===")
    test_generate_lexical_pool()

    print("=== format_lexical_pool test ===")
    test_format_lexical_pool()

    print("=== generate_rules test ===")
    test_generate_rules()

if __name__ == "__main__":
    main()