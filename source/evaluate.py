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

# Load model
tokenizer = AutoTokenizer.from_pretrained("FacebookAI/roberta-large-mnli")
model = AutoModelForSequenceClassification.from_pretrained("FacebookAI/roberta-large-mnli")
model.eval()

def evaluate(pairs, model, tokenizer, key_name=None, results_dir=None):
    
    # Determine base directory for outputs
    if results_dir:
        os.makedirs(results_dir, exist_ok=True)
        base_dir = results_dir
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Initialize storage for example labels and probabilities
    labels = []
    all_probs = []
    
    # Retrieve all class labels for detailed scoring
    classes = [model.config.id2label[i] for i in range(len(model.config.id2label))]
    
    # Construct results filename using key_name if provided
    results_filename = f"results_{key_name}.txt" if key_name else "results.txt"
    out_path = os.path.join(base_dir, results_filename)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    print(f"Saving results to {out_path}")
    
    with open(out_path, 'w') as out_file:
        for idx, (premise, hypothesis) in enumerate(pairs):
            inputs = tokenizer(premise, hypothesis, return_tensors="pt", truncation=True)
            with torch.no_grad():
                logits = model(**inputs).logits
            probs = torch.softmax(logits, dim=1)[0]
            pred_id = torch.argmax(probs).item()
            label = model.config.id2label[pred_id]

            # Write numbered example and all class probabilities
            out_file.write(f"Example {idx+1}:\n")
            out_file.write(f"Premise: {premise}\nHypothesis: {hypothesis}\n")
            out_file.write(f"Prediction: {label}\n")
            out_file.write("Scores:\n")
            for cls_name, prob_val in zip(classes, probs.tolist()):
                out_file.write(f"  {cls_name}: {prob_val:.4f}\n")
            out_file.write("\n")
            labels.append(f"Example {idx+1}")
            all_probs.append(probs.tolist())
    
    # Generate and save plot
    plot(labels, all_probs, model, base_dir, key_name)
