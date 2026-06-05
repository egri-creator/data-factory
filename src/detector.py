"""Quality gate: statistical analysis that simulates AI detectors.
Scores each text on humanness dimensions and filters out machine-like text."""

import re
import math
from collections import Counter


class QualityGate:
    def __init__(self, min_score=0.6):
        self.min_score = min_score

    def analyze(self, text):
        """Full analysis - returns dict with all metrics and pass/fail"""
        metrics = {
            "burstiness": self._burstiness(text),
            "sentence_start_diversity": self._sentence_start_diversity(text),
            "type_token_ratio": self._type_token_ratio(text),
            "filler_density": self._filler_density(text),
            "sentence_length_cv": self._sentence_length_cv(text),
            "error_pattern_score": self._error_pattern_score(text),
            "discourse_marker_density": self._discourse_marker_density(text),
            "punctuation_variety": self._punctuation_variety(text),
            "has_self_correction": self._has_self_correction(text),
            "has_contradiction": self._has_contradiction(text),
            "has_digression": self._has_digression(text),
        }
        metrics["humanness_score"] = self._compute_humanness(metrics)
        metrics["pass"] = metrics["humanness_score"] >= self.min_score
        return metrics

    def _burstiness(self, text):
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) < 3:
            return 0.3
        lengths = [len(s.split()) for s in sentences]
        mean = sum(lengths) / len(lengths)
        if mean == 0:
            return 0
        variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
        cv = math.sqrt(variance) / mean
        clamped = min(max(cv / 1.2, 0), 1)
        return round(clamped, 3)

    def _sentence_start_diversity(self, text):
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) < 3:
            return 0.3
        starts = [s.strip()[:5].lower() if s.strip() else "" for s in sentences]
        unique = len(set(starts))
        ratio = unique / len(sentences)
        return round(min(ratio * 1.5, 1.0), 3)

    def _type_token_ratio(self, text):
        words = text.lower().split()
        if len(words) < 5:
            return 0
        unique = len(set(words))
        ratio = unique / len(words)
        clamped = min(ratio / 0.7, 1.0)
        return round(clamped, 3)

    _FILLER_WORDS = {
        "eh", "bueno", "o sea", "entonces", "mira", "digamos", "vamos",
        "pues", "ah", "mmm", "a ver", "total", "claro", "obvio", "sabes",
        "verdad", "no sé", "cómo te explico", "la cosa es", "es que",
        "tipo", "como que", "o sea que", "neta", "la verdad", "sinceramente",
        "quizás", "tal vez", "a lo mejor", "capaz", "igual y",
    }

    def _filler_density(self, text):
        lower = text.lower()
        count = 0
        for filler in self._FILLER_WORDS:
            count += lower.count(filler)
        words = len(text.split())
        if words == 0:
            return 0
        density = count / words
        clamped = min(density * 20, 1.0)
        return round(clamped, 3)

    def _sentence_length_cv(self, text):
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) < 3:
            return 0.3
        lengths = [len(s.split()) for s in sentences]
        mean = sum(lengths) / len(lengths)
        if mean == 0:
            return 0
        std = math.sqrt(sum((l - mean) ** 2 for l in lengths) / len(lengths))
        cv = std / mean
        if cv < 0.3:
            return 0.1
        if cv > 1.5:
            return 1.0
        return round((cv - 0.3) / 1.2, 3)

    def _error_pattern_score(self, text):
        """Score based on presence of human-like errors (higher = more human)"""
        score = 0.0
        checks = 0

        if re.search(r'[a-z][A-Z]', text):
            score += 1
            checks += 1
        if re.search(r'\b(haber|echo|tubo|valla|aya|tambien|solo)\b', text.lower()):
            score += 1
            checks += 1
        if "..." in text:
            score += 1
            checks += 1
        if re.search(r'\b\w{1,2}\b', text):
            score += 1
            checks += 1
        if re.search(r'(?<=[.,;])(?=[A-Za-zÁÉÍÓÚáéíóú])', text):
            score += 1
            checks += 1

        return round(score / max(checks, 1), 3) if checks > 0 else 0.5

    def _discourse_marker_density(self, text):
        markers = [
            "entonces", "después", "antes", "mientras", "aunque",
            "sin embargo", "por eso", "además", "también", "porque",
            "así que", "entonces", "luego", "finalmente", "por cierto",
            "total que", "el caso es que", "resulta que",
        ]
        lower = text.lower()
        count = sum(lower.count(m) for m in markers)
        words = len(text.split())
        if words == 0:
            return 0
        density = count / words
        return round(min(density * 30, 1.0), 3)

    def _punctuation_variety(self, text):
        chars = text
        if len(chars) == 0:
            return 0
        punct_counts = Counter(c for c in chars if c in ".,!?;:-()\"'¡¿...")
        if not punct_counts:
            return 0
        total_punct = sum(punct_counts.values())
        unique_types = len(punct_counts)
        variety = (unique_types / 10) * (total_punct / len(chars) * 20)
        return round(min(variety, 1.0), 3)

    def _has_self_correction(self, text):
        patterns = [
            r'o sea\b', r'digo\b', r'más bien\b', r'mejor dicho\b',
            r'bueno\b.*\bquiero decir', r'no, espera\b', r'quise decir\b',
            r'en realidad\b', r'la verdad es que\b',
        ]
        return 1.0 if any(re.search(p, text.lower()) for p in patterns) else 0.0

    def _has_contradiction(self, text):
        patterns = [
            r'(pero|aunque|sin embargo).*(no sé|quien sabe|tal vez|quizá)',
            r'o tal vez no',
            r'igual y me equivoco',
            r'capaz que estoy mal',
            r'ya ni sé',
        ]
        return 1.0 if any(re.search(p, text.lower()) for p in patterns) else 0.0

    def _has_digression(self, text):
        patterns = [
            r'\([^)]*\)', r'—[^—]*—', r'cambiando de tema',
            r'esto me recuerda', r'por cierto', r'ah y',
            r'no sé por qué cuento esto',
        ]
        return 1.0 if any(re.search(p, text.lower()) for p in patterns) else 0.0

    def _compute_humanness(self, metrics):
        weights = {
            "burstiness": 0.15,
            "sentence_start_diversity": 0.10,
            "type_token_ratio": 0.10,
            "filler_density": 0.10,
            "sentence_length_cv": 0.10,
            "error_pattern_score": 0.10,
            "discourse_marker_density": 0.10,
            "punctuation_variety": 0.05,
            "has_self_correction": 0.07,
            "has_contradiction": 0.07,
            "has_digression": 0.06,
        }
        score = sum(metrics[k] * w for k, w in weights.items() if k in metrics)
        return round(min(score, 1.0), 3)


def dataset_quality_report(examples):
    """Generate a quality report for the entire dataset"""
    if not examples:
        return {"error": "no examples"}
    gate = QualityGate()
    scores = []
    failures = []
    for ex in examples:
        analysis = gate.analyze(ex["text"])
        scores.append(analysis["humanness_score"])
        if not analysis["pass"]:
            failures.append(ex.get("id", "?"))
    avg = sum(scores) / len(scores) if scores else 0
    return {
        "mean_humanness": round(avg, 3),
        "min_score": round(min(scores), 3),
        "max_score": round(max(scores), 3),
        "pass_rate": round(1 - len(failures) / len(examples), 3),
        "failed_ids": failures,
        "dataset_passes": avg >= 0.6 and len(failures) / len(examples) < 0.2,
    }
