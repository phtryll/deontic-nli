import os
import torch
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import entropy
from matplotlib.ticker import MaxNLocator
from transformers import AutoModelForSequenceClassification, AutoTokenizer, logging

# Silence expected unused weight warnings from transformers
logging.set_verbosity_error()


def load_nli_model(model_name: str):
    """Helper function to load a tokenizer and NLI model by name from HuggingFace."""

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.eval()

    return tokenizer, model


def plot_bar(probs, classes, base_dir, key_name):
    """Helper function to plot model's output for each example."""

    # Path to store the figure
    path = os.path.join(base_dir, f"graph_{key_name}.png")
    print(f"Saving plot to {path}")

    # Convert probabilities to pandas DataFrame
    df = pd.DataFrame(probs, columns=classes, index=range(len(probs)))

    # Create figure
    figure = df.plot(kind='bar', rot=0, stacked=True)
    figure.set(title=key_name, xlabel="Example IDs", ylabel="Probabilities")
    figure.xaxis.set_major_locator(MaxNLocator(nbins=20))
    
    # Save
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()


def plot_mustache(all_entropies, results_dir):
    """Helper function to plot model output distributions for each grammar across all examples."""

    # Set path
    path = os.path.join(results_dir, "cross_grammar_entropy_boxplot.png")
    print(f"Saving mustache plot to {path}")

    # Convert to DataFrame
    df = pd.DataFrame(all_entropies)

    # Rename columns to numeric indices for x-axis
    index_map = {i + 1: name for i, name in enumerate(df.columns)}
    df.columns = list(index_map.keys())

    # Create boxplot
    figure = df.boxplot(grid=False, patch_artist=True)
    figure.set(title="Cross-Grammar Entropy", xlabel="Sub-grammars", ylabel="Entropy (bits)")

    # Add legend using the mapping
    legend_patches = [mpatches.Patch(label=f"{i}: {name}") for i, name in index_map.items()]
    figure.legend(
        handles=legend_patches,
        title="Legend",
        loc="center right",
        bbox_to_anchor=(-0.115, 0.5),
        fontsize="small"
    )

    # Save plot
    plt.savefig(path, bbox_inches="tight", dpi=300)
    plt.close()


def evaluate(pairs, model_name, batch_size=16):
    """
    Evaluation pipeline for a set of premise/hypothesis paris.
    For now the model loaded is roberta-large-mnli.
    Outputs a txt file with the output of the model for each pair,
    as well as plots aggregating the results.
    """

    # Set tokenizer and model
    tokenizer, model = load_nli_model(model_name)

    # Retrieve all class labels (i.e. 'Contradiction', 'Entailment', 'Neutral')
    id2label = model.config.id2label # We use it later on
    classes = list(id2label.values())

    # Store evaluation results
    results = []

    # Main evaluation loop over batches of examples
    # for batch_start in tqdm(range(0, len(pairs), batch_size), desc="Evaluating over batches"):
    for batch_start in range(0, len(pairs), batch_size):

        # Create batches of example pairs
        batch = pairs[batch_start : batch_start + batch_size]
        premises, hypotheses = map(list, zip(*batch))

        # Prepare the inputs for the model
        inputs = tokenizer(
            premises,
            hypotheses,
            return_tensors="pt",
            padding=True,
            truncation=True
        )

        # Forward pass
        with torch.inference_mode():
            logits = model(**inputs).logits

        # Get the probabilities and the predicted labels
        batch_probs = torch.softmax(logits, dim=1)
        pred_ids = batch_probs.argmax(dim=1)
        
        # Each example is a tuple with premise, hypothesis, probabilities vector and predicted label
        results.extend(
            (premise, hypothesis, id2label[int(pred_id)], probs.tolist())
            for (premise, hypothesis), pred_id, probs in zip(batch, pred_ids, batch_probs)
        )
    
    return results, classes


def compute_entropies(pairs, model_name, batch_size=16, base=2):
    """Evaluate a set of pairs and return only the entropy vector."""

    results, _ = evaluate(pairs, model_name, batch_size)
    entropies = [entropy(probs, base=base) for (_, _, _, probs) in results]
    
    return entropies


def write_to_file(results, classes, key_name, results_dir):

    # Identify the path where the results file will be stored
    out_path = os.path.join(results_dir, f"results_{key_name}.txt")
    print(f"Saving results to {out_path}")

    # Write the results in a .txt file
    with open(out_path, "w") as out_file:

        # Loop over each example pair and write in the file
        for idx, (premise, hypothesis, label, probs) in enumerate(results):
            out_file.write(f"Example {idx}:\n")
            out_file.write(f"Premise: {premise}\nHypothesis: {hypothesis}\n")
            out_file.write(f"Prediction: {label}\n")
            out_file.write("Scores:\n")
            out_file.writelines(f"\t{cls}: {prob:.4f}\n" for cls, prob in zip(classes, probs))
            out_file.write("\n")

    # Plot the results
    plot_bar([probs for (_, _, _, probs) in results], classes, results_dir, key_name)