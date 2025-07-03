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

# CLI tool for generating deontic logic examples and lexical resources
def main():
    parser = argparse.ArgumentParser(description="Deontic NLI CLI utility")

    # Option to print the underlying CFG grammar rules
    parser.add_argument("--show-grammar", action="store_true", help="Print the CFG grammar")

    # Option to generate N examples from the grammar. Mode can be 'cfg' for uniform or 'pcfg' for probabilistic generation.
    parser.add_argument(
        "--generate-examples",
        nargs=2,
        metavar=("N", "MODE"),
        help="Generate N examples; MODE should be 'cfg' or 'pcfg'",
        default=None,
    )

    # Option to generate a pool of lexical items for each category using the masked language model
    parser.add_argument(
        "--generate-lexical-pool",
        nargs='?',
        const=20,
        type=int,
        default=None,
        metavar="N",
        help="Generate N lexical items for specific categories"
    )
    
    # Option to generate N lexical rules using the masked language model and CamemBERT
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
        
        # Display the CFG grammar to the user
        print("\n----Context-free grammar----\n")
        print(grammar)

    if args.generate_examples:
        
        # Parse and validate generate-examples arguments
        count_str, mode = args.generate_examples
        
        try:
            count = int(count_str)
        except ValueError:
            parser.error("generate-examples requires an integer count and mode 'cfg' or 'pcfg'")
        
        mode_lower = mode.lower()
        
        if mode_lower not in ("cfg", "pcfg"):
            parser.error("generate-examples mode must be 'cfg' or 'pcfg'")
        
        use_probabilistic = (mode_lower == "pcfg")
        
        # Create a CFG instance with probabilistic mode if requested
        grammar_to_use = CFG(rules=my_rules, axiom="S", probabilistic=use_probabilistic)
        
        print(f"----Generated examples ({mode_lower.upper()})----\n")
        generate_examples(grammar_to_use, count, print_tree=False)

    if args.generate_rules:
        
        # Generate lexical inference rules using the language model
        generate_rules(prompts, tokenizer, model, top_k=args.generate_rules, labels=labels)
    
    if args.generate_lexical_pool:
        
        # Generate and print lexical category pools
        pool = generate_lexical_pool(prompts, tokenizer, model, top_k=args.generate_lexical_pool)
        
        for category, items in pool.items():
            for item in items:  
                print(f"{category}: {item}")

if __name__ == "__main__":
    main()
