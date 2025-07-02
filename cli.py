import argparse
import logging
from transformers import AutoTokenizer, AutoModelForMaskedLM
from source.generate import generate_examples, generate_rules
from source.generate_utils import generate_lexical_pool
from source.cfg import CFG
from resources.axiom_obrm import my_rules
from resources.model_prompts import prompts, labels

# Suppress useless transformers messages
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

def main():
    parser = argparse.ArgumentParser(description="Deontic NLI CLI utility")
    parser.add_argument("--show-grammar", action="store_true", help="Print the CFG grammar")

    parser.add_argument(
        "--generate-examples",
        nargs='?',
        const=20,
        type=int,
        default=None,
        metavar="N",
        help="Generate N rules with specific non-terminal symbols"
    )

    parser.add_argument(
        "--generate-lexical-pool",
        nargs='?',
        const=20,
        type=int,
        default=None,
        metavar="N",
        help="Generate N lexical items for specific categories"
    )
    
    parser.add_argument(
        "--generate-rules",
        nargs='?',
        const=20,
        type=int,
        default=None,
        metavar="N",
        help="Generate N lexical rules using CamemBERT"
    )

    args = parser.parse_args()

    # Initialize tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained("FacebookAI/xlm-roberta-large")
    model = AutoModelForMaskedLM.from_pretrained("FacebookAI/xlm-roberta-large")
    
    # Initialize grammar
    grammar = CFG(rules=my_rules, axiom="S")

    if args.show_grammar:
        print("\n----Context-free grammar----\n")
        print(grammar)

    if args.generate_examples:
        print("----Generated examples----\n")
        generate_examples(grammar, args.generate_examples, print_tree=False)

    if args.generate_rules:
        generate_rules(prompts, tokenizer, model, top_k=args.generate_rules, labels=labels)
    
    if args.generate_lexical_pool:
        pool = generate_lexical_pool(prompts, tokenizer, model, top_k=args.generate_lexical_pool)
        for category, items in pool.items():
            for item in items:  
                print(f"{category}: {item}")

if __name__ == "__main__":
    main()
