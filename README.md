# Data Factory v2 — Datasets Sintéticos Indetectables

Generador automático de datasets sintéticos de **calidad humana** para entrenar IAs.
Cada texto pasa por una capa multi-modelo + humanización avanzada para que **ningún detector de IA pueda distinguirlo de texto escrito por humanos**.

## 🚀 Características

### 🎯 Calidad Humana Absoluta
- **25 nichos** especializados con prompts hiper-realistas
- **Capa anti-detección**: burstiness, perplejidad variable, imperfecciones lingüísticas naturales
- **Multi-modelo**: usa aleatoriamente Mistral-7B, Gemma-2, Phi-3 + fallback local
- **Humanización extrema**: typos realistas, muletillas culturales, contradicciones, emociones

### 📦 Multi-Formato
- `jsonl` — Formato genérico
- `csv` — Para hojas de cálculo
- `alpaca` — Formato Alpaca (instruction/input/output)
- `sharegpt` — Conversaciones multi-turno
- `openai` — Formato de fine-tuning de OpenAI
- `chatml` — Formato ChatML

### 🛡️ Calidad y Protección
- **Filtro automático** de calidad (longitud, coherencia)
- **Deduplicación** por similitud Jaccard
- **Split** train/validation/test automático
- **Watermark** integrado para protección de copyright
- **Dataset card** completa para Hugging Face

## 📋 Nichos disponibles

| Categoría | Nichos |
|---|---|
| salud | medical, therapy_session, fitness_log |
| tecnología | tech_support, dev_discussion, tech_tutorial, gaming_community |
| opiniones | local_reviews, product_comparison, movie_review, book_club, restaurant_review |
| educación | educational_tutoring, academic_writing |
| legal | legal_consultation |
| finanzas | financial_advice |
| atención al cliente | customer_service |
| negocios | business_email |
| carrera | job_interview, career_advice |
| personal | journal_entry, personal_story |
| cocina | cooking_recipe |
| viajes | travel_review |
| vivienda | real_estate |
| familia | parenting_forum |
| política | political_opinion |
| ocio | hobby_discussion |
| mascotas | pet_care |
| hogar | home_improvement |

## ⚙️ Configuración

Copia `.env.example` a `.env` y configura:

```env
# Hugging Face (necesario solo para subir datasets)
HF_USERNAME=tu_usuario
HF_TOKEN=tu_token

# Generación
DATASET_NICHE=medical
EXAMPLES_PER_RUN=500
HUMANIZATION_LEVEL=extreme

# Modelos (todos gratuitos)
USE_HF=true
HF_MODELS=mistralai/Mistral-7B-Instruct-v0.2,google/gemma-2-2b-it,microsoft/Phi-3-mini-4k-instruct
```

## 🖥️ Uso

```bash
# Listar nichos disponibles
python generate_dataset.py --list-niches

# Generar un nicho
python generate_dataset.py --niche medical --num 500

# Generar con formatos específicos
python generate_dataset.py --niche tech_support --formats jsonl,openai

# Generar TODOS los nichos
python generate_dataset.py --niche all --num 1000

# Generar y subir a Hugging Face
python generate_dataset.py --niche medical --num 500 --upload

# Control de humanización
python generate_dataset.py --niche local_reviews -H extreme
```

## 🏗️ Arquitectura

```
generate_dataset.py          ← Entry point con CLI
src/
├── config.py                ← Configuración y validación
├── templates.py             ← 25 nichos con prompts y variables
├── humanizer.py             ← Capa anti-detección de IA
├── models.py                ← Multi-proveedor (HF + Ollama + local)
├── quality.py               ← Filtros, dedup, estadísticas, watermark
├── formats.py               ← Exportación multi-formato
└── pipeline.py              ← Orquestación completa
```

## 📊 Output

Cada generación produce una carpeta con:

```
datasets/medical_dataset_20250101_120000/
├── data.jsonl
├── data.csv
├── data_alpaca.jsonl
├── data_sharegpt.jsonl
├── data_openai.jsonl
├── data_chatml.jsonl
├── README.md                ← Dataset card para Hugging Face
├── metadata.json            ← Metadatos completos
├── train/                   ← Split de entrenamiento
│   ├── data.jsonl
│   └── ...
├── validation/              ← Split de validación
│   └── ...
└── test/                    ← Split de prueba
    └── ...
```

## 🚀 Deploy en Render

El archivo `render.yaml` configura un cron job que ejecuta cada 6 horas automáticamente y sube los datasets a Hugging Face.

```bash
# En Render.com: New → Blueprint → conectar repo
```

## 💰 Coste CERO

- **Hugging Face Inference API**: gratuita (con rate limits)
- **Render cron jobs**: tier gratuito
- **Ollama local**: completamente gratis
- **Fallback local**: funciona sin internet ni APIs

No necesitas pagar nada para generar datasets de calidad profesional.

## 📜 Licencia

MIT. Los datasets generados son libres para uso comercial.
