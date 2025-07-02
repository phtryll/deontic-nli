import logging
from transformers import AutoTokenizer, AutoModelForMaskedLM
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

from source.generate_utils import fill_mask, generate_lexical_pool

def test_fill_mask():
    tokenizer = AutoTokenizer.from_pretrained("FacebookAI/xlm-roberta-large")
    model = AutoModelForMaskedLM.from_pretrained("FacebookAI/xlm-roberta-large")

    prompt = "The city of <mask> is in the country of <mask>."
    print("Testing fill_mask on:", prompt)
    beams = fill_mask(prompt, tokenizer, model, top_k=20)
    for i, (tokens, score) in enumerate(beams, 1):
        print(f"  Beam {i}: {tokens}  (joint score={score:.5f})")
    print()

def test_generate_lexical_pool():
    tokenizer = AutoTokenizer.from_pretrained("FacebookAI/xlm-roberta-large")
    model = AutoModelForMaskedLM.from_pretrained("FacebookAI/xlm-roberta-large")

    prompts = {
        "LOCATIONS": [
            "The city of <mask> is in the country of <mask>.",
            "We went to <mask>, and visited the little town of <mask>. It was beautiful!"
        ]
    }

    print("Testing generate_lexical_pool...")
    pool = generate_lexical_pool(prompts, tokenizer, model, top_k=10)
    for category, items in pool.items():
        print(f"{category}:")
        for item in items:
            print("  ", item)
    print()

def main():
    print("=== fill_mask test ===")
    test_fill_mask()

    print("=== generate_lexical_pool test ===")
    test_generate_lexical_pool()

if __name__ == "__main__":
    main()