import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from transformers import AutoModelForSequenceClassification, AutoTokenizer, logging

# Silence expected unused weight warnings from transformers
logging.set_verbosity_error()

def plot(labels, all_probs, model, base_dir, key_name=None):
    """Plot stacked score distributions and save as JPEG in base_dir."""
    
    classes = [model.config.id2label[i] for i in range(len(model.config.id2label))]
    all_probs = np.array(all_probs)
    x = np.arange(len(labels))
    bottom = np.zeros(len(labels))
    
    for i, cls in enumerate(classes):
        plt.bar(x, all_probs[:, i], bottom=bottom, width=0.5, label=cls)
        bottom += all_probs[:, i]
    ax = plt.gca()
    # Place ticks at every 5th example: 5, 10, 15...
    step = 5
    if len(labels) >= step:
        positions = x[step-1::step]
        tick_labels = [str(pos+1) for pos in positions]
        ax.set_xticks(positions)
        ax.set_xticklabels(tick_labels)
        ax.tick_params(axis='x', which='major', labelsize=8)
    else:
        ax.set_xticks(x)
        ax.set_xticklabels([str(i+1) for i in x])
    plt.ylabel('Probability')
    # Set plot title to the provided key name
    if key_name:
        plt.title(key_name)
    plt.legend()
   
    # Construct filename using key_name if provided
    filename = f"graph_{key_name}.jpeg" if key_name else "graph.jpeg"
    jpg_path = os.path.join(base_dir, filename)
    plt.savefig(jpg_path, format='jpeg', dpi=300)
    plt.close()
    print(f"Saved plot to {jpg_path}")


# Load model in inference mode
tokenizer = AutoTokenizer.from_pretrained("FacebookAI/roberta-large-mnli")
model = AutoModelForSequenceClassification.from_pretrained("FacebookAI/roberta-large-mnli")
model.eval()


def evaluate(pairs, model, tokenizer, key_name, results_dir, batch_size=16):
    """
    Evaluation pipeline for a set of premise/hypothesis paris.
    For now the model loaded is roberta-large-mnli.
    Outputs a txt file with the output of the model for each pair,
    as well as plots aggregating the results.
    """

    # Initialize storage for example labels and probabilities
    results = []
    labels = []
    all_probs = []
    
    # Retrieve all class labels (i.e. 'Contradiction', 'Entailment', 'Neutral')
    id2label = model.config.id2label # We use it later on
    classes = list(id2label.values())
    
    # Identify the path where the results file will be stored
    out_path = os.path.join(results_dir, f"results_{key_name}.txt")
    print(f"Saving results to {out_path}")
    
    # Main evaluation loop over batches of examples
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

    # Write the results in a .txt file
    with open(out_path, "w") as out_file:

        # Loop over each example pair and write in the file
        for idx, (premise, hypothesis, label, probs) in enumerate(results):
            out_file.write(f"Example {idx+1}:\n")
            out_file.write(f"Premise: {premise}\nHypothesis: {hypothesis}\n")
            out_file.write(f"Prediction: {label}\n")
            out_file.write("Scores:\n")
            for cls_name, prob_val in zip(classes, probs):
                out_file.write(f"\t{cls_name}: {prob_val:.4f}\n")
            out_file.write("\n")
    
    # Generate and save plot
    labels = [f"Example {i+1}" for i in range(len(results))]
    all_probs = [probs for (_, _, _, probs) in results]
    plot(labels, all_probs, model, results_dir, key_name)
