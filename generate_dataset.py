#!/usr/bin/env python3
"""
Data Factory v2 — Generador de datasets sintéticos indetectables
Uso: python generate_dataset.py [--niche N] [--num N] [--formats F] [--list-niches]
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import Config, VALID_NICHES
from src.templates import NICHE_CATEGORIES
from src.templates import NICHES
from src.pipeline import run_pipeline, upload_to_hub


def main():
    parser = argparse.ArgumentParser(
        description="Data Factory v2 — Generador de datasets sintéticos indetectables",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python generate_dataset.py --niche medical --num 1000
  python generate_dataset.py --niche tech_support --formats jsonl,openai
  python generate_dataset.py --list-niches
  python generate_dataset.py --niche all --num 5000
        """
    )
    parser.add_argument("--niche", "-n", help="Nicho a generar")
    parser.add_argument("--num", "-N", type=int, help="Número de ejemplos")
    parser.add_argument("--formats", "-f", help="Formatos de exportación (jsonl,csv,alpaca,sharegpt,openai,chatml)")
    parser.add_argument("--humanization", "-H", choices=["light", "medium", "extreme"], help="Nivel de humanización")
    parser.add_argument("--output", "-o", help="Directorio de salida")
    parser.add_argument("--list-niches", action="store_true", help="Listar nichos disponibles")
    parser.add_argument("--upload", action="store_true", help="Subir a Hugging Face Hub")

    args = parser.parse_args()

    if args.list_niches:
        print("\nNichos disponibles:\n")
        for cat, niches in sorted(NICHE_CATEGORIES.items()):
            print(f"  [{cat}]")
            for n in niches:
                info = NICHES[n]
                print(f"    • {n:35s} — {info['description']}")
            print()
        print(f"  Usa --niche all para generar TODOS los nichos secuencialmente")
        return

    if args.niche == "all":
        niches_to_run = VALID_NICHES
    elif args.niche:
        if args.niche not in VALID_NICHES:
            print(f"Nicho '{args.niche}' no válido. Usa --list-niches para ver disponibles.")
            sys.exit(1)
        niches_to_run = [args.niche]
    else:
        config = Config()
        config.validate()
        niches_to_run = [config.niche]

    for niche in niches_to_run:
        cfg = Config()
        cfg.niche = niche
        if args.num:
            cfg.num_examples = args.num
        if args.formats:
            cfg.formats = [f.strip() for f in args.formats.split(",")]
        if args.humanization:
            cfg.humanization_level = args.humanization
        if args.output:
            cfg.output_dir = args.output

        print(f"\n{'#'*60}")
        print(f"  Generando: {niche}")
        print(f"  Ejemplos:  {cfg.num_examples}")
        print(f"{'#'*60}")

        result = run_pipeline(cfg)
        if result is None:
            print(f"  Error generando {niche}")
            continue

        if args.upload:
            upload_to_hub(cfg, result)

    print("\n¡Todo listo! Los datasets están listos para vender.")


if __name__ == "__main__":
    main()
