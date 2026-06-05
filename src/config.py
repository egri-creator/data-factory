import os
from dataclasses import dataclass, field
from typing import List
from dotenv import load_dotenv

load_dotenv()

VALID_NICHES = [
    "medical", "tech_support", "local_reviews", "legal_consultation",
    "financial_advice", "educational_tutoring", "therapy_session",
    "customer_service", "dev_discussion", "academic_writing",
    "business_email", "job_interview", "journal_entry",
    "cooking_recipe", "travel_review", "fitness_log",
    "real_estate", "parenting_forum", "political_opinion",
    "hobby_discussion", "restaurant_review", "tech_tutorial",
    "personal_story", "product_comparison", "career_advice",
    "movie_review", "book_club", "gaming_community",
    "pet_care", "home_improvement"
]

@dataclass
class Config:
    hf_token: str = os.getenv("HF_TOKEN", "")
    hf_username: str = os.getenv("HF_USERNAME", "")

    niche: str = os.getenv("DATASET_NICHE", "medical")
    num_examples: int = int(os.getenv("EXAMPLES_PER_RUN", "500"))

    use_hf: bool = os.getenv("USE_HF", "true").lower() == "true"
    use_ollama: bool = os.getenv("USE_OLLAMA", "false").lower() == "true"
    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3")

    hf_models: List[str] = field(default_factory=lambda: [
        m.strip() for m in os.getenv("HF_MODELS", "mistralai/Mistral-7B-Instruct-v0.2,google/gemma-2-2b-it,microsoft/Phi-3-mini-4k-instruct").split(",") if m.strip()
    ])

    min_length: int = int(os.getenv("MIN_LENGTH", "30"))
    max_length: int = int(os.getenv("MAX_LENGTH", "3000"))
    dedup_threshold: float = float(os.getenv("DEDUP_THRESHOLD", "0.82"))

    output_dir: str = os.getenv("OUTPUT_DIR", "./datasets")
    formats: List[str] = field(default_factory=lambda: [
        f.strip() for f in os.getenv("EXPORT_FORMATS", "jsonl,csv,alpaca,sharegpt,openai,chatml").split(",") if f.strip()
    ])
    val_split: float = float(os.getenv("VAL_SPLIT", "0.1"))
    test_split: float = float(os.getenv("TEST_SPLIT", "0.1"))

    humanization_level: str = os.getenv("HUMANIZATION_LEVEL", "extreme")
    watermark_key: str = os.getenv("WATERMARK_KEY", "datafactory-v1")
    regenerate_failed: bool = os.getenv("REGENERATE_FAILED", "true").lower() == "true"

    @property
    def train_split(self):
        return 1.0 - self.val_split - self.test_split

    def validate(self):
        errors = []
        if self.niche not in VALID_NICHES:
            errors.append(f"Niche '{self.niche}' no válido. Válidos: {', '.join(VALID_NICHES)}")
        if self.num_examples < 1:
            errors.append("EXAMPLES_PER_RUN debe ser >= 1")
        if self.val_split + self.test_split >= 1.0:
            errors.append("val_split + test_split debe ser < 1.0")
        if self.humanization_level not in ("light", "medium", "extreme"):
            errors.append("HUMANIZATION_LEVEL debe ser: light, medium, extreme")
        if self.dedup_threshold < 0 or self.dedup_threshold > 1:
            errors.append("DEDUP_THRESHOLD debe estar entre 0 y 1")
        if errors:
            raise ValueError("\n".join(errors))
        return True
