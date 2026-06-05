import random
import time
import requests
from .templates import NICHES
from .humanizer import Humanizer

HF_API_URL = "https://api-inference.huggingface.co/models/{model}"

class BaseProvider:
    def __init__(self, config):
        self.config = config
        niche_info = NICHES.get(config.niche, {})
        self.prompts = niche_info.get("prompts", [])
        self.variables = niche_info.get("variables", {})

    def generate(self, example_id):
        raise NotImplementedError

    def _build_prompt(self):
        template = random.choice(self.prompts)
        kwargs = {}
        for var_name, var_values in self.variables.items():
            kwargs[var_name] = random.choice(var_values) if var_values else f"{{{var_name}}}"
        return template.format(**kwargs)

    def _finalize(self, raw_text, country=None):
        humanizer = Humanizer(level=self.config.humanization_level, country=country or "México")
        text = humanizer.humanize(raw_text)
        return {
            "id": 0,
            "text": text,
            "niche": self.config.niche,
            "source_model": self.__class__.__name__,
        }


class HFProvider(BaseProvider):
    def __init__(self, config):
        super().__init__(config)
        self.models = config.hf_models
        self.token = config.hf_token

    def generate(self, example_id):
        if not self.token:
            return self._fallback_generate(example_id)
        model = random.choice(self.models)
        prompt = self._build_prompt()
        url = HF_API_URL.format(model=model)
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": random.randint(100, 300),
                "temperature": random.uniform(0.7, 1.1),
                "top_p": random.uniform(0.85, 0.98),
                "do_sample": True,
                "return_full_text": False,
                "repetition_penalty": random.uniform(1.0, 1.15),
            }
        }
        for attempt in range(3):
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=60)
                if resp.status_code == 503:
                    time.sleep(5)
                    continue
                resp.raise_for_status()
                result = resp.json()
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get("generated_text", prompt)
                else:
                    text = prompt
                result = self._finalize(text, country=self._pick_country())
                result["id"] = example_id
                return result
            except Exception as e:
                if attempt < 2:
                    time.sleep(2 ** attempt * 2)
                continue
        return self._fallback_generate(example_id)

    def _pick_country(self):
        countries = self.config.humanizer_countries if hasattr(self.config, 'humanizer_countries') else NICHES.get(self.config.niche, {}).get("variables", {}).get("country", ["México"])
        if isinstance(countries, list):
            return random.choice(countries) if countries else "México"
        return "México"

    def _fallback_generate(self, example_id):
        return FallbackProvider(self.config).generate(example_id)


class FallbackProvider(BaseProvider):
    def __init__(self, config):
        super().__init__(config)
        self._build_fallback_pool()

    def _build_fallback_pool(self):
        self._starts = [
            "La verdad es que", "Mira, te cuento que", "Resulta que",
            "Fíjate que", "El caso es que", "O sea que", "Pues mira",
            "La cosa está así:", "Te explico:", "Todo empezó cuando",
            "Lo que pasa es que", "Imagínate que", "A mi parecer",
            "Sinceramente", "La neta es que", "Para ser honesto",
            "Según yo", "Desde mi punto de vista", "Hablando claro",
            "Te juro que", "No te miento si te digo que", "Voy al grano:",
            "En resumen,", "Al grano:", "Déjame contarte que",
            "No sabes lo que pasó:", "Prepárate:", "Qué te cuento:",
        ]
        self._mids = [
            "el otro día me pasó algo curioso con",
            "estuve pensando en lo de",
            "nunca había visto algo así con",
            "me sorprendió bastante que",
            "resulta que todo era por culpa de",
            "al final terminó siendo más sencillo de lo que creía porque",
            "le pregunté a varias personas y todas me dijeron que",
            "después de darle muchas vueltas, me di cuenta de que",
            "lo más gracioso de todo es que",
            "para mi sorpresa, descubrí que",
            "lo que nadie te dice es que",
            "después de todo, resulta que",
            "lo peor de todo fue cuando",
            "el momento clave fue cuando",
            "justo cuando pensé que ya, pasó que",
            "al final del día lo que importa es que",
            "lo que más me llamó la atención fue que",
            "si te soy sincero, lo que pasó fue que",
            "no sabía qué esperar pero resultó que",
            "para no hacerte el cuento largo, pasó que",
            "entre otras cosas, pasó que",
            "y lo mejor de todo fue que",
            "y para rematar, resulta que",
            "cuestión que",
        ]
        self._ends = [
            "y al final todo salió bien, creo.",
            "pero quién sabe, la verdad.",
            "y así fue como terminó todo.",
            "total, que para eso ni me hubiera preocupado.",
            "y aquí estoy, contándote esto sin mucho sentido.",
            "en fin, cosas que pasan.",
            "y ya, no tengo más que decir.",
            "o al menos esa es mi experiencia.",
            "pero bueno, cada quien su experiencia.",
            "y así, sin más.",
            "y eso es todo lo que tengo que decir al respecto.",
            "y mira, así son las cosas.",
            "uno nunca sabe, la verdad.",
            "y pues así pasa.",
            "y bueno, esa es la historia.",
        ]
        self._niche_phrases = {
            "medical": [
                "el doctor me dijo que no era para tanto pero igual me preocupé",
                "me recetaron algo que no recuerdo cómo se llama",
                "la verdad es que los síntomas eran raros, no coincidían con nada",
                "en la farmacia me dieron algo diferente a lo que pedí",
                "después de varios exámenes resultó que no era nada grave",
                "el médico me preguntó si había comido algo raro y no supe qué responder",
                "me mandaron a hacer análisis y me perdí el resultado dos semanas",
                "la enfermera me atendió bien aunque el consultorio era un desastre",
                "estuve esperando como dos horas solo para que me dijeran que era estrés",
                "me recetaron algo tan caro que ni lo compré al final",
                "el doctor ni me miró, solo escribió en la computadora todo el tiempo",
                "me dijeron que tenía algo pero no entendí bien el nombre",
                "ya llevo meses con esto y nadie me da una respuesta clara",
                "me hicieron preguntas muy personales y no venían al caso",
                "resulta que todo era por el medicamento que ya estaba tomando",
            ],
            "tech_support": [
                "ya intenté apagarlo y encenderlo como 5 veces",
                "el técnico me pidió que hiciera algo y no funcionó",
                "después de la actualización todo se puso peor",
                "resulta que el problema era un cable que estaba mal conectado",
                "llamé al soporte y me tuvieron en espera 40 minutos para nada",
                "el sistema se puso lento de repente sin ninguna razón aparente",
                "un compañero dijo que a él también le pasó y que se resolvió solo",
                "intenté seguir los pasos del manual pero estaban en otro idioma",
                "el chat de soporte me pidió información que ya había dado tres veces",
                "revisé los foros y nadie tiene una solución para esto",
                "desde que instalaron la actualización todo va más lento que nunca",
                "el técnico vino, lo miró, dijo 'esto es complicado' y se fue",
                "borraron mi configuración cuando hicieron el mantenimiento",
                "no entiendo por qué lo programaron así, no tiene lógica",
                "la página web tiene un error que sale solo cuando ya llevas horas trabajando",
            ],
            "local_reviews": [
                "la verdad es que esperaba más por el precio",
                "lo compré porque lo vi en TikTok y pues, ya sabes",
                "mis amigas me dijeron que era bueno y no me arrepiento",
                "llegó en una caja toda maltratada pero el producto estaba bien",
                "la calidad es buena pero el empaque deja mucho que desear",
                "lo usé una semana y ya está fallando, no sé si pedir cambio",
                "lo compré en oferta y por ese precio no me quejo",
                "las instrucciones no se entendían y tuve que ver un video",
                "pedí el color equivocado por no leer bien pero igual me gustó",
                "tardó un montón en llegar pero cuando llegó valió la pena",
                "mi vecino tiene el mismo y le funciona mejor, chance es suerte",
                "lo devolví porque no era lo que esperaba pero el proceso fue fácil",
                "se parece mucho a la foto del anuncio, eso sí se agradece",
                "lo compré como regalo y a la persona le encantó",
                "es la segunda vez que compro esta marca y nunca me ha fallado",
            ],
        }
        for niche_key in list(NICHES.keys()):
            self._niche_phrases.setdefault(niche_key, [])

    def generate(self, example_id):
        niche = self.config.niche
        niche_phrases = self._niche_phrases.get(niche, [])
        all_phrases = niche_phrases + self._mids
        random.shuffle(all_phrases)
        num_sentences = max(4, min(10, random.randint(4, 10)))
        connectors = [
            "Además,", "Por otro lado,", "También,", "Igual,", "Eso sí,",
            "En cambio,", "Lo bueno es que", "Lo malo fue que", "La cosa es que",
            "El detalle es que", "Eso sí,", "Al final,",
        ]
        parts = []
        used_starters = []
        used_mids = []
        for i in range(num_sentences):
            available_starts = [s for s in self._starts if s not in used_starters]
            if not available_starts:
                used_starters = []
                available_starts = self._starts
            start = random.choice(available_starts)
            used_starters.append(start)
            available_mids = [m for m in all_phrases if m not in used_mids]
            if not available_mids:
                used_mids = []
                available_mids = all_phrases
            mid = random.choice(available_mids)
            used_mids.append(mid)
            end = random.choice(self._ends)
            if i == 0:
                parts.append(f"{start} {mid} {end}")
            else:
                connector = random.choice(connectors)
                parts.append(f"{connector} {start[0].lower() + start[1:]} {mid} {end}")
        text = " ".join(parts)
        country = "México"
        if niche in NICHES:
            countries = NICHES[niche].get("variables", {}).get("country", ["México"])
            if isinstance(countries, list) and countries:
                country = random.choice(countries)
        humanizer = Humanizer(level=self.config.humanization_level, country=country)
        text = humanizer.humanize(text)
        return {
            "id": example_id,
            "text": text,
            "niche": niche,
            "source_model": "FallbackProvider",
        }


class OllamaProvider(BaseProvider):
    def __init__(self, config):
        super().__init__(config)
        self.url = config.ollama_url.rstrip("/") + "/api/generate"
        self.model = config.ollama_model

    def generate(self, example_id):
        prompt = self._build_prompt()
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": random.uniform(0.7, 1.1),
                "top_p": random.uniform(0.85, 0.98),
                "num_predict": random.randint(100, 300),
            }
        }
        try:
            resp = requests.post(self.url, json=payload, timeout=120)
            resp.raise_for_status()
            text = resp.json().get("response", prompt)
        except Exception:
            text = prompt
        result = self._finalize(text, country="México")
        result["id"] = example_id
        return result


def create_providers(config):
    providers = []
    if config.use_hf and config.hf_token:
        providers.append(HFProvider(config))
    if config.use_ollama:
        providers.append(OllamaProvider(config))
    providers.append(FallbackProvider(config))
    return providers
