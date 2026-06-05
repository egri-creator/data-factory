"""Humanizer v3 — Anti-detection engine with cognitive patterns + real error database.
12+ layers that make AI text statistically indistinguishable from human writing."""

import random
import re
import math

# ========== COGNITIVE PATTERNS ==========

TOPIC_DRIFTS = [
    " (bueno, esto me desvía del tema pero hablando de eso me acordé de cuando...)",
    " —cambiando de tema radicalmente, aunque no tanto—",
    " (esto no viene al caso pero justo ayer hablaba de algo similar con un amigo y...)",
    " (todo esto me recuerda que tengo que hacer una llamada, pero sigo)",
    " aunque eso me hace pensar en otra cosa que me pasó...",
    " —y mira que yo no soy de divagar, pero—",
]

FALSE_STARTS = [
    "La cosa... bueno, déjame empezar de nuevo.",
    "No, espera, mejor dicho...",
    "Es que... cómo te explico...",
    "Bueno, el punto es que...",
    "O sea... no, déjame ver cómo explicarlo.",
    "A ver, empecemos por el principio:",
]

SPIRAL_THOUGHTS = [
    " y vuelvo a lo mismo, no sé por qué le doy tantas vueltas",
    " ya sé que me estoy repitiendo, pero es que...",
    " y es que mientras más pienso, más me enredo",
    " y todo esto para decir que al final no sé",
]

EPISTEMIC_DOWNGRADES = [
    " Bueno, o al menos eso creo, porque la verdad ya no sé.",
    " Igual y me equivoco, no soy experto en esto.",
    " O tal vez no, qué sé yo.",
    " Aunque quién sabe, cada quien habla como le va.",
    " O eso entendí yo, capaz y no es así.",
    " En fin, no tengo idea la verdad.",
]

NARRATIVE_EMBEDDINGS = [
    " —esto me acuerda de cuando me pasó algo parecido—",
    " (ah, y hablando de eso, una vez...)",
    " como decía mi abuela, el que sabe sabe",
]

# ========== REAL SPANISH ERROR DATABASE ==========
# These are REAL common mistakes Spanish speakers make,
# organized by type, not random character swaps

REAL_TYPOS_QWERTY = {
    "buneo": ("bueno", 0.3), "vomo": ("como", 0.2), "adios": ("adiós", 0.2),
    "muchas": ("muchas", 0), "caza": ("casa", 0.15), "hasi": ("haci", 0.2),
    "querer": ("querer", 0), "tambien": ("también", 0.4),
    "segun": ("según", 0.3), "algo": ("algo", 0),
}

COMMON_SPELLING_MISTAKES = [
    ("a ver", "haber"), ("haber", "a ver"), ("echo", "hecho"),
    ("hecho", "echo"), ("tubo", "tuvo"), ("valla", "vaya"),
    ("aya", "haya"), ("ay", "hay"), ("hay", "ay"),
    ("por que", "porque"), ("si no", "sino"),
    ("demas", "demás"), ("sobre todo", "sobretodo"),
    ("con que", "conque"), ("tambien", "también"),
    ("solo", "sólo"), ("este", "éste"),
]

ACCENT_ERRORS = [
    ("medico", "médico"), ("medico", "médico"), ("caracter", "carácter"),
    ("ingles", "inglés"), ("ingles", "inglés"), ("arbol", "árbol"),
    ("lapiz", "lápiz"), ("facil", "fácil"), ("dificil", "difícil"),
    ("util", "útil"), ("automatico", "automático"),
    ("publico", "público"), ("tipico", "típico"),
    ("periodico", "periódico"), ("musica", "música"),
]

# ========== EXISTING CONSTANTS (enhanced) ==========

FILLERS = [
    "eh...", "bueno...", "o sea...", "entonces...", "mira...",
    "digamos...", "vamos...", "este...", "pues...", "ah...",
    "mmm...", "a ver...", "y nada...", "total...", "claro...",
    "obvio...", "sabes?", "o no?", "verdad?", "no sé...",
    "cómo te explico...", "la cosa es...", "pues mira...",
    "a ver si me explico...", "vamos a ver...", "es que fíjate que...",
    "te soy sincero...", "la neta...", "para serte honesto...",
]

SELF_CORRECTIONS = [
    "o sea, {replacement}",
    "bueno, más bien {replacement}",
    "digo, {replacement}",
    "no, espera, {replacement}",
    "mejor dicho, {replacement}",
    "{replacement}... es decir, no sé",
    "o mejor {replacement}",
    "bueno, en realidad {replacement}",
    "cómo te dijera... {replacement}",
]

SHORT_SENTENCES = [
    "Y ya.", "No sé.", "Bueno.", "Total.", "En fin.",
    "Qué sé yo.", "Da igual.", "Ni modo.", "Ya ves.",
    "Cosas que pasan.", "Y así.", "Para variar.",
    "Clásico.", "Típico.", "Qué le vamos a hacer.",
    "Ni hablar.", "Ya qué.", "Ya ni sé.",
    "En fin, al caso.", "Total que sí.",
    "Y bue, qué se le va a hacer.",
]

EMOTIONAL_EXCLAMATIONS = [
    " (y la verdad me dio una rabia...)", " ¡qué frustración!",
    " en serio, no sabes lo que fue eso",
    " y yo así como de ¿en serio?",
    " fue un momento muy awkward",
    " no sabes el coraje que me dio",
    " y yo tipo... no puede ser",
    " fue muy heavy todo",
    " y yo así de... no mames",
    " te juro que no podía creerlo",
    " fue una experiencia, cómo te explico, bien random",
    " y yo tipo okay... y ahora qué",
    " la verdad no sabía si reír o llorar",
]

CONTRADICTIONS = [
    " Bueno, o tal vez no, no sé.",
    " O al menos eso creo yo, igual y me equivoco.",
    " Aunque la verdad ya ni sé qué pensar.",
    " Pero igual y es al revés, quién sabe.",
    " O no, capaz que estoy mal.",
    " En fin, no tengo idea la verdad.",
    " Pero eso es lo que yo pienso, cada quien su perspectiva.",
    " O al menos esa es mi versión de los hechos.",
]

FRAGMENTS = [
    "Cosas que pasan.", "Ni modo.", "Qué le vamos a hacer.",
    "Así nomás.", "En fin.", "Para qué seguir.",
    "Da igual.", "Total.", "Y punto.", "Ya qué.",
    "Ni hablar.", "Qué sé yo.",
    "Puras cosas.", "Así es esto.",
]

REGIONAL_VARIATIONS = {
    "México": [
        ("ordenador", "computadora"), ("vale", "va"), ("conducir", "manejar"),
        ("coche", "carro"), ("gafas", "lentes"), ("nevera", "refri"),
        ("piso", "departamento"), ("garbanzos", "chícharos"),
        ("judías verdes", "ejotes"), ("tarta", "pastel"),
    ],
    "Argentina": [
        ("ordenador", "computadora"), ("vale", "dale"), ("conducir", "manejar"),
        ("coche", "auto"), ("gafas", "anteojos"), ("nevera", "heladera"),
        ("piso", "departamento"), ("fresa", "frutilla"), ("judías", "porotos"),
        ("tarta", "torta"), ("melocotón", "durazno"),
    ],
    "España": [
        ("computadora", "ordenador"), ("manejar", "conducir"),
        ("carro", "coche"), ("lentes", "gafas"), ("refri", "nevera"),
        ("departamento", "piso"), ("jugo", "zumo"),
        ("plátano", "banana"), ("agarrar", "coger"),
    ],
    "Colombia": [
        ("ordenador", "computador"), ("judías", "frijoles"),
        ("melocotón", "durazno"), ("tarta", "ponqué"),
    ],
    "Chile": [
        ("ordenador", "computador"), ("coche", "auto"),
        ("melocotón", "durazno"), ("judías", "porotos"),
    ],
    "Perú": [
        ("ordenador", "computadora"), ("judías", "frejoles"),
        ("melocotón", "durazno"), ("tarta", "torta"),
    ],
}

COUNTRY_FILLERS = {
    "México": ["ése", "güey", "neta", "chido", "madre", "wey"],
    "Argentina": ["che", "boludo", "dale", "tipo", "genial"],
    "España": ["tío", "mola", "guay", "vale", "hostia"],
    "Colombia": ["parce", "qué más", "ve", "bacano", "chévere"],
    "Chile": ["weón", "cachay", "po", "bacán", "fome"],
    "Perú": ["causa", "pata", "chévere", "asuuu"],
    "Venezuela": ["pana", "chévere", "vale", "vaina"],
    "Ecuador": ["mijo", "chuta", "qué bestia"],
    "Uruguay": ["bo", "ta", "re", "cantegril"],
    "Costa Rica": ["mae", "tuanis", "pura vida"],
}

QWERTY_ADJACENCY = {
    "q": "w", "w": "qe", "e": "wr", "r": "et", "t": "ry", "y": "tu",
    "u": "yi", "i": "uo", "o": "ip", "p": "o",
    "a": "s", "s": "ad", "d": "sf", "f": "dg", "g": "fh", "h": "gj",
    "j": "hk", "k": "jl", "l": "k",
    "z": "x", "x": "zc", "c": "xv", "v": "cb", "b": "vn", "n": "bm",
    "m": "n",
}


class Humanizer:
    def __init__(self, level="extreme", country=None):
        self.level = level
        self.country = country
        self.chance_mult = {"light": 0.4, "medium": 0.7, "extreme": 1.0}[level]
        self._cognitive_style = random.choice(["analytical", "emotional", "chaotic", "dry"])

    def humanize(self, text):
        if not text or not isinstance(text, str):
            return text
        if self.level == "light":
            return self._light_humanize(text)
        return self._extreme_humanize(text)

    def _light_humanize(self, text):
        if random.random() < 0.15 * self.chance_mult:
            text = self._add_filler(text)
        if random.random() < 0.1 * self.chance_mult:
            text = self._inject_real_errors(text)
        if random.random() < 0.1 * self.chance_mult:
            text = self._vary_punctuation(text)
        return text

    def _extreme_humanize(self, text):
        text = self._inject_burstiness(text)
        text = self._add_filler(text)
        text = self._inject_real_errors(text)
        text = self._vary_punctuation(text)
        text = self._add_self_correction(text)
        text = self._inconsistent_caps(text)
        text = self._add_regional_flavor(text)
        text = self._cognitive_layer(text)
        if random.random() < 0.35:
            text = self._add_digression(text)
        if random.random() < 0.25:
            text = self._inject_emotion(text)
        if random.random() < 0.2:
            text = self._add_contradiction(text)
        if random.random() < 0.15:
            text = self._sentence_fragment(text)
        if random.random() < 0.12:
            text = self._run_on_sentence(text)
        if random.random() < 0.1:
            text = self._false_start(text)
        if random.random() < 0.08:
            text = self._spiral_thought(text)
        if random.random() < 0.15:
            text = self._narrative_embedding(text)
        text = self._qwerty_typo(text)
        return text

    # ===== COGNITIVE PATTERNS =====

    def _cognitive_layer(self, text):
        style = self._cognitive_style
        if style == "emotional":
            text = self._inject_emotion(text)
            if random.random() < 0.3:
                text = text + random.choice([" 😅", " 🥲", " 🤷", ""])
        elif style == "chaotic":
            if random.random() < 0.3:
                text = self._false_start(text)
            if random.random() < 0.3:
                text = self._add_digression(text)
        elif style == "analytical":
            if random.random() < 0.2:
                text = text + " Analizándolo bien, creo que..."
        elif style == "dry":
            pass
        return text

    def _false_start(self, text):
        if random.random() < 0.3 * self.chance_mult:
            fs = random.choice(FALSE_STARTS)
            sentences = re.split(r'(?<=[.!?])\s+', text)
            if len(sentences) > 2:
                idx = random.randint(1, len(sentences) - 1)
                sentences[idx] = fs + " " + sentences[idx]
                text = " ".join(sentences)
        return text

    def _spiral_thought(self, text):
        if random.random() < 0.3 * self.chance_mult:
            st = random.choice(SPIRAL_THOUGHTS)
            text = text + st
        return text

    def _narrative_embedding(self, text):
        if random.random() < 0.3 * self.chance_mult:
            ne = random.choice(NARRATIVE_EMBEDDINGS)
            sentences = re.split(r'(?<=[.!?])\s+', text)
            if len(sentences) > 2:
                idx = random.randint(0, len(sentences) - 2)
                sentences[idx] = sentences[idx] + ne
                text = " ".join(sentences)
        return text

    def _epistemic_downgrade(self, text):
        if random.random() < 0.3 * self.chance_mult:
            ed = random.choice(EPISTEMIC_DOWNGRADES)
            text = text.rstrip(".!?") + ed
        return text

    # ===== REAL ERROR INJECTION =====

    def _inject_real_errors(self, text):
        if random.random() < 0.25 * self.chance_mult:
            text = self._spelling_mistake(text)
        if random.random() < 0.15 * self.chance_mult:
            text = self._accent_error(text)
        return text

    def _spelling_mistake(self, text):
        correct, wrong = random.choice(COMMON_SPELLING_MISTAKES)
        if random.random() < 0.5:
            correct, wrong = wrong, correct
        if correct.lower() in text.lower():
            pattern = re.compile(re.escape(correct), re.IGNORECASE)
            if random.random() < 0.4:
                text = pattern.sub(wrong, text, count=1)
        return text

    def _accent_error(self, text):
        wrong, correct = random.choice(ACCENT_ERRORS)
        pattern = re.compile(r'\b' + re.escape(wrong) + r'\b', re.IGNORECASE)
        if pattern.search(text):
            if random.random() < 0.3:
                text = pattern.sub(wrong, text, count=1)
        return text

    def _qwerty_typo(self, text):
        words = text.split()
        if len(words) < 5:
            return text
        num_typos = max(1, int(len(words) * 0.02 * self.chance_mult))
        for _ in range(num_typos):
            idx = random.randint(0, len(words) - 1)
            word = words[idx]
            if len(word) < 4:
                continue
            char_idx = random.randint(1, len(word) - 2)
            char = word[char_idx].lower()
            if char in QWERTY_ADJACENCY:
                repl = random.choice(QWERTY_ADJACENCY[char])
                if word[char_idx].isupper():
                    repl = repl.upper()
                words[idx] = word[:char_idx] + repl + word[char_idx + 1:]
        return " ".join(words)

    # ===== EXISTING METHODS (enhanced) =====

    def _inject_burstiness(self, text):
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) < 2:
            return text
        result = []
        for s in sentences:
            if random.random() < 0.2:
                s = s.strip()
                if len(s) > 30 and random.random() < 0.3:
                    split_point = random.randint(len(s) // 3, len(s) // 2)
                    while split_point < len(s) and s[split_point] != " ":
                        split_point += 1
                    if split_point < len(s) - 5:
                        s = s[:split_point] + "." + s[split_point:]
                elif len(s) > 5 and random.random() < 0.2:
                    result.append(random.choice(SHORT_SENTENCES))
            result.append(s)
        return " ".join(result)

    def _add_filler(self, text):
        if random.random() < 0.35 * self.chance_mult:
            filler = random.choice(FILLERS)
            if random.random() < 0.5:
                text = filler + " " + text[0].lower() + text[1:] if text else text
            else:
                text = text + " " + filler
        if random.random() < 0.2 * self.chance_mult:
            sentences = re.split(r'(?<=[.!?])\s+', text)
            if len(sentences) > 2:
                idx = random.randint(1, len(sentences) - 2)
                sentences.insert(idx, random.choice(FILLERS))
                text = " ".join(sentences)
        return text

    def _vary_punctuation(self, text):
        if random.random() < 0.12 * self.chance_mult and len(text) > 20:
            n = random.randint(1, 2)
            text = text.replace(", ", ",", n)
        if random.random() < 0.08 * self.chance_mult:
            sentences = re.split(r'(?<=[.!?])\s+', text)
            if sentences and len(sentences) > 1:
                last = sentences[-1]
                if last and last[-1] in ".!?" and random.random() < 0.3:
                    sentences[-1] = last[:-1]
                text = " ".join(sentences)
        if random.random() < 0.05 * self.chance_mult:
            text = text.replace("...", "..", 1)
        if random.random() < 0.05 * self.chance_mult:
            text = text.replace("!", "¡!" if random.random() < 0.5 else "!")
        return text

    def _add_self_correction(self, text):
        if random.random() < 0.15 * self.chance_mult:
            words = text.split()
            if len(words) > 6:
                idx = random.randint(2, len(words) - 3)
                replacement = random.choice(words[max(0, idx - 3):idx + 3])
                correction = random.choice(SELF_CORRECTIONS).format(replacement=replacement)
                words.insert(idx, correction)
                text = " ".join(words)
        return text

    def _inconsistent_caps(self, text):
        if random.random() < 0.12 * self.chance_mult:
            sentences = re.split(r'(?<=[.!?])\s+', text)
            if len(sentences) > 1:
                idx = random.randint(1, len(sentences) - 1)
                if sentences[idx] and sentences[idx][0].isalpha():
                    if random.random() < 0.5:
                        sentences[idx] = sentences[idx][0].lower() + sentences[idx][1:]
                    else:
                        sentences[idx] = sentences[idx][0].upper() + sentences[idx][1:]
                text = " ".join(sentences)
        return text

    def _add_regional_flavor(self, text):
        if not self.country or self.country not in REGIONAL_VARIATIONS:
            return text
        if random.random() < 0.3 * self.chance_mult:
            for orig, repl in REGIONAL_VARIATIONS[self.country]:
                if orig in text.lower() and random.random() < 0.4:
                    try:
                        text = re.sub(re.escape(orig), repl, text, flags=re.IGNORECASE)
                    except Exception:
                        pass
                    break
        if self.country in COUNTRY_FILLERS and random.random() < 0.25:
            country_word = random.choice(COUNTRY_FILLERS[self.country])
            sentences = re.split(r'(?<=[.!?])\s+', text)
            if sentences and random.random() < 0.5:
                last = sentences[-1]
                if last and not last.endswith(country_word):
                    sentences[-1] = last + ", " + country_word if random.random() < 0.5 else country_word + ", " + last
                    text = " ".join(sentences)
        return text

    def _add_digression(self, text):
        digressions = TOPIC_DRIFTS + [
            " (bueno, esto no viene al caso pero para que te des una idea)",
            " (esto me recuerda que tengo que hacer algo mañana)",
            " aunque, pensándolo bien, no estoy tan seguro",
            " (no sé por qué cuento esto pero bueno)",
            " y mira que yo no soy de quejarme pero",
        ]
        if random.random() < 0.3 * self.chance_mult:
            sentences = re.split(r'(?<=[.!?])\s+', text)
            if len(sentences) > 2:
                idx = random.randint(1, len(sentences) - 1)
                insertion = random.choice(digressions)
                sentences[idx] = sentences[idx] + insertion
                text = " ".join(sentences)
        return text

    def _inject_emotion(self, text):
        if random.random() < 0.4 * self.chance_mult:
            text = text + random.choice(EMOTIONAL_EXCLAMATIONS)
        return text

    def _add_contradiction(self, text):
        if random.random() < 0.4 * self.chance_mult:
            text = text.rstrip(".!?") + random.choice(CONTRADICTIONS)
        return text

    def _sentence_fragment(self, text):
        if random.random() < 0.4 * self.chance_mult:
            text = text + " " + random.choice(FRAGMENTS)
        return text

    def _run_on_sentence(self, text):
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) > 2:
            idx = random.randint(0, len(sentences) - 2)
            combined = sentences[idx].rstrip(".!?") + " y " + sentences[idx + 1][0].lower() + sentences[idx + 1][1:]
            sentences[idx] = combined
            sentences.pop(idx + 1)
            text = " ".join(sentences)
        return text

    def compute_burstiness_score(self, text):
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) < 2:
            return 0
        lengths = [len(s.split()) for s in sentences]
        mean = sum(lengths) / len(lengths)
        variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
        return math.sqrt(variance) / mean if mean > 0 else 0

    def compute_perplexity_proxy(self, text):
        words = text.lower().split()
        if len(words) < 5:
            return 0
        bigrams = {}
        for i in range(len(words) - 1):
            bg = (words[i], words[i + 1])
            bigrams[bg] = bigrams.get(bg, 0) + 1
        if not bigrams:
            return 0
        avg_freq = sum(bigrams.values()) / len(bigrams)
        return avg_freq

    def analyze_humanness(self, text):
        burstiness = self.compute_burstiness_score(text)
        perp_proxy = self.compute_perplexity_proxy(text)
        has_imperfections = any([
            "..." in text,
            "eh" in text.lower(),
            "o sea" in text.lower(),
            any(text.lower().endswith(f) for f in ["no sé", "bueno", "total", "y ya"]),
        ])
        score = min(1.0, burstiness / 0.8 * 0.5 + (1.0 - perp_proxy / 10) * 0.3 + (0.2 if has_imperfections else 0))
        return {
            "burstiness": round(burstiness, 3),
            "perplexity_proxy": round(perp_proxy, 3),
            "has_imperfections": has_imperfections,
            "humanness_score": round(score, 3),
        }
