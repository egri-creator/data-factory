import re
import hashlib
import statistics
from collections import Counter

def filter_examples(examples, min_len=80, max_len=3000):
    """Remove too short, too long, or empty texts"""
    filtered = []
    for ex in examples:
        t = ex.get("text", "")
        if not t or not isinstance(t, str):
            continue
        length = len(t.split())
        if length < min_len or length > max_len:
            continue
        if len(t) < 20:
            continue
        filtered.append(ex)
    return filtered


def deduplicate(examples, threshold=0.82):
    """Remove duplicates and near-duplicates using Jaccard similarity on n-grams"""
    def ngrams(text, n=3):
        words = text.lower().split()
        return set(" ".join(words[i:i + n]) for i in range(len(words) - n + 1))

    def jaccard(a, b):
        if not a or not b:
            return 0
        return len(a & b) / len(a | b)

    if not examples:
        return examples

    ngram_sets = [ngrams(ex["text"]) for ex in examples]
    keep = [True] * len(examples)

    for i in range(len(examples)):
        if not keep[i]:
            continue
        for j in range(i + 1, len(examples)):
            if not keep[j]:
                continue
            sim = jaccard(ngram_sets[i], ngram_sets[j])
            if sim >= threshold:
                keep[j] = False

    return [ex for i, ex in enumerate(examples) if keep[i]]


def compute_stats(examples):
    """Compute detailed statistics about the dataset"""
    if not examples:
        return {"error": "no examples"}
    texts = [ex["text"] for ex in examples]
    word_counts = [len(t.split()) for t in texts]
    char_counts = [len(t) for t in texts]
    sentence_counts = [len(re.split(r'(?<=[.!?])\s+', t)) for t in texts]
    all_words = " ".join(texts).lower().split()
    word_freq = Counter(all_words)

    return {
        "total_examples": len(examples),
        "total_words": sum(word_counts),
        "total_chars": sum(char_counts),
        "avg_words_per_example": round(statistics.mean(word_counts), 1),
        "median_words": round(statistics.median(word_counts), 1),
        "min_words": min(word_counts),
        "max_words": max(word_counts),
        "std_words": round(statistics.stdev(word_counts), 1) if len(word_counts) > 1 else 0,
        "avg_sentences": round(statistics.mean(sentence_counts), 1),
        "avg_chars": round(statistics.mean(char_counts), 1),
        "vocabulary_size": len(word_freq),
        "top_20_words": word_freq.most_common(20),
        "single_occurrence_words": sum(1 for v in word_freq.values() if v == 1),
    }


def generate_dataset_card(examples, config, stats, dataset_name):
    """Generate a comprehensive Hugging Face dataset card"""
    niche_info = None
    from .templates import NICHES
    niche_info = NICHES.get(config.niche, {"description": config.niche, "category": "general"})

    train_pct = config.train_split * 100
    val_pct = config.val_split * 100
    test_pct = config.test_split * 100

    card = f"""---
language:
- es
license: mit
tags:
- synthetic
- {config.niche}
- spanish
- data-factory
- ai-training
pretty_name: "{dataset_name}"
size_categories:
- {_size_category(stats['total_examples'])}
task_categories:
- text-generation
- text-classification
---

# {dataset_name}

## Descripción

Dataset sintético de alta calidad para entrenar modelos de lenguaje en el nicho **{config.niche}** ({niche_info.get('description', config.niche)}).

Generado con Data Factory — sistema multi-modelo con capa de humanización avanzada para garantizar textura lingüística natural y realista.

## Usos recomendados

- Fine-tuning de modelos de lenguaje (LLMs)
- Entrenamiento de clasificadores de texto
- Generación de texto condicionada
- Evaluación de modelos en dominio específico

## Formato

Cada ejemplo contiene:
- `id`: identificador único
- `text`: texto generado y humanizado
- `niche`: categoría del dataset
- `source_model`: modelo que generó el texto
- `split`: train / validation / test

## Estadísticas

| Métrica | Valor |
|---|---|
| Total ejemplos | {stats['total_examples']} |
| Total palabras | {stats['total_words']:,} |
| Promedio palabras/ejemplo | {stats['avg_words_per_example']} |
| Vocabulario único | {stats['vocabulary_size']:,} |
| Palabras de 1 ocurrencia | {stats['single_occurrence_words']:,} |
| Train / Val / Test | {train_pct:.0f}% / {val_pct:.0f}% / {test_pct:.0f}% |

## Licencia

MIT. Libre para uso comercial, investigación y fine-tuning.

## Origen

100% sintético. Generado por Data Factory combinando múltiples modelos de lenguaje con una capa de humanización avanzada. Sin datos de usuarios reales ni contenido con copyright.

## Consideraciones éticas

Este dataset es completamente sintético y no contiene información personal real. Sin embargo, se recomienda revisar los sesgos potenciales antes de usar en producción.
"""
    return card


def _size_category(n):
    if n < 1000:
        return "n<1K"
    if n < 10000:
        return "1K<n<10K"
    if n < 100000:
        return "10K<n<100K"
    return "100K<n<1M"


def watermark_text(text, key="datafactory-v1"):
    """Embed an invisible watermark via controlled synonym replacement."""
    watermark_map = {
        "muy": "bastante",
        "bueno": "buenazo",
        "casa": "hogar",
        "amigo": "compadre",
        "comida": "manduca",
        "trabajo": "chamba",
        "dinero": "lana",
        "bonito": "lindo",
        "grande": "enormote",
        "pequeño": "chiquitín",
    }
    seed = sum(ord(c) for c in key)
    rng = random.Random(seed)
    words = text.split()
    result = []
    for w in words:
        clean = w.lower().strip(".,!?;:")
        if clean in watermark_map and rng.random() < 0.3:
            repl = watermark_map[clean]
            if w[0].isupper():
                repl = repl.capitalize()
            result.append(repl)
        else:
            result.append(w)
    return " ".join(result)


import random


def signature_hash(text):
    """Create a dataset signature for integrity verification"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
