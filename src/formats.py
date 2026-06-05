import json
import csv
import os

def save_jsonl(examples, path):
    with open(path, "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

def save_csv(examples, path):
    if not examples:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(examples[0].keys()))
        writer.writeheader()
        writer.writerows(examples)

def save_alpaca(examples, path):
    """Alpaca format: {instruction, input, output}"""
    entries = []
    for ex in examples:
        entries.append({
            "instruction": f"Genera un texto realista en español sobre {ex['niche']}.",
            "input": "",
            "output": ex["text"],
        })
    with open(path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

def save_sharegpt(examples, path):
    """ShareGPT format: [{from, value}] conversation turns"""
    from collections import OrderedDict
    entries = []
    for ex in examples:
        text = ex["text"]
        sentences = text.split(". ")
        if len(sentences) < 2:
            entries.append({
                "conversations": [
                    {"from": "human", "value": f"Cuéntame algo sobre {ex['niche']}."},
                    {"from": "gpt", "value": text},
                ]
            })
        else:
            mid = len(sentences) // 2
            human_part = ". ".join(sentences[:mid])
            gpt_part = ". ".join(sentences[mid:])
            entries.append({
                "conversations": [
                    {"from": "human", "value": human_part.strip()},
                    {"from": "gpt", "value": gpt_part.strip()},
                ]
            })
    with open(path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

def save_openai(examples, path):
    """OpenAI fine-tuning format: {messages: [{role, content}]}"""
    entries = []
    for ex in examples:
        entries.append({
            "messages": [
                {"role": "user", "content": f"Genera contenido en español sobre {ex['niche']}."},
                {"role": "assistant", "content": ex["text"]},
            ]
        })
    with open(path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

def save_chatml(examples, path):
    """ChatML format: <|im_start|>role\ncontent<|im_end|>"""
    entries = []
    for ex in examples:
        content = f"<|im_start|>user\nGenera un texto realista sobre {ex['niche']}.<|im_end|>\n<|im_start|>assistant\n{ex['text']}<|im_end|>"
        entries.append({"text": content})
    with open(path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

FORMAT_FUNCTIONS = {
    "jsonl": ("data.jsonl", save_jsonl),
    "csv": ("data.csv", save_csv),
    "alpaca": ("data_alpaca.jsonl", save_alpaca),
    "sharegpt": ("data_sharegpt.jsonl", save_sharegpt),
    "openai": ("data_openai.jsonl", save_openai),
    "chatml": ("data_chatml.jsonl", save_chatml),
}

def export_all(examples, output_dir, formats=None):
    """Export examples in multiple formats. Returns dict of format -> path."""
    if formats is None:
        formats = list(FORMAT_FUNCTIONS.keys())
    os.makedirs(output_dir, exist_ok=True)
    result = {}
    for fmt in formats:
        if fmt in FORMAT_FUNCTIONS:
            fname, func = FORMAT_FUNCTIONS[fmt]
            path = os.path.join(output_dir, fname)
            func(examples, path)
            result[fmt] = path
    return result

def split_dataset(examples, train_pct=0.8, val_pct=0.1, test_pct=0.1):
    """Split examples into train/val/test"""
    import random
    shuffled = list(examples)
    random.shuffle(shuffled)
    n = len(shuffled)
    n_train = int(n * train_pct)
    n_val = int(n * val_pct)
    train = shuffled[:n_train]
    val = shuffled[n_train:n_train + n_val]
    test = shuffled[n_train + n_val:]
    for split_name, split_data in [("train", train), ("validation", val), ("test", test)]:
        for ex in split_data:
            ex["split"] = split_name
    return train, val, test

def save_splits(examples, output_dir, formats=None):
    """Save dataset splits in multiple formats"""
    if formats is None:
        formats = list(FORMAT_FUNCTIONS.keys())
    splits_dir = os.path.join(output_dir, "splits")
    os.makedirs(splits_dir, exist_ok=True)
    for split_name, split_data in examples:
        split_out = os.path.join(splits_dir, split_name)
        os.makedirs(split_out, exist_ok=True)
        export_all(split_data, split_out, formats)
