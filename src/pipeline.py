import os
import json
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from .templates import NICHES
from .models import create_providers, FallbackProvider
from .quality import filter_examples, deduplicate, compute_stats, generate_dataset_card, watermark_text, signature_hash
from .formats import export_all, split_dataset
from .detector import QualityGate, dataset_quality_report


def generate_example(provider, example_id):
    try:
        return provider.generate(example_id)
    except Exception as e:
        from .models import FallbackProvider
        return FallbackProvider(provider.config).generate(example_id)


def run_pipeline(config):
    """Main pipeline: generate, filter, deduplicate, split, export, upload"""
    print(f"\n{'='*60}")
    print(f"  DATA FACTORY v2 — Pipeline Completo")
    print(f"  Nicho: {config.niche}")
    print(f"  Ejemplos solicitados: {config.num_examples}")
    print(f"  Nivel humanización: {config.humanization_level}")
    print(f"  Formatos: {', '.join(config.formats)}")
    print(f"{'='*60}\n")

    niche_info = NICHES.get(config.niche)
    if not niche_info:
        print(f"ERROR: Nicho '{config.niche}' no encontrado.")
        return None

    providers = create_providers(config)
    print(f"  Proveedores cargados: {len(providers)}")
    for p in providers:
        print(f"    - {p.__class__.__name__}")

    num_providers = len(providers)
    per_provider = max(1, config.num_examples // num_providers)
    extra = config.num_examples % num_providers

    examples = []
    example_id = 0

    start_time = time.time()
    for pi, provider in enumerate(providers):
        count = per_provider + (1 if pi < extra else 0)
        print(f"\n  [{provider.__class__.__name__}] generando {count} ejemplos...")
        batch_start = time.time()
        batch_ids = list(range(example_id, example_id + count))
        completed = 0
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(generate_example, provider, bid): bid for bid in batch_ids}
            for future in as_completed(futures):
                try:
                    ex = future.result()
                    if ex and ex.get("text"):
                        examples.append(ex)
                except Exception:
                    pass
                completed += 1
                if completed % 10 == 0 or completed == count:
                    elapsed = time.time() - batch_start
                    rate = completed / elapsed if elapsed > 0 else 0
                    print(f"    {completed}/{count} — {rate:.1f} ej/s")
        example_id += count

    raw_count = len(examples)
    print(f"\n  Generados: {raw_count} ejemplos ({(time.time() - start_time) / 60:.1f} min)")

    examples = filter_examples(examples, config.min_length, config.max_length)
    filtered_count = len(examples)
    print(f"  Tras filtro de calidad: {filtered_count} (eliminados {raw_count - filtered_count})")

    examples = deduplicate(examples, config.dedup_threshold)
    dedup_count = len(examples)
    print(f"  Tras deduplicación: {dedup_count} (eliminados {filtered_count - dedup_count})")

    if config.watermark_key:
        for ex in examples:
            ex["text"] = watermark_text(ex["text"], config.watermark_key)

    for ex in examples:
        ex["dataset_signature"] = signature_hash(ex["text"])

    quality_gate = QualityGate(min_score=0.55)
    gate_results = []
    regenerated = 0
    for i, ex in enumerate(examples):
        analysis = quality_gate.analyze(ex["text"])
        ex["humanness_score"] = analysis["humanness_score"]
        gate_results.append(analysis)
        if not analysis["pass"]:
            if config.regenerate_failed:
                fb = FallbackProvider(config)
                new_ex = fb.generate(ex["id"] + 10000)
                if new_ex and new_ex.get("text"):
                    new_analysis = quality_gate.analyze(new_ex["text"])
                    if new_analysis["pass"] or new_analysis["humanness_score"] > analysis["humanness_score"]:
                        examples[i] = new_ex
                        examples[i]["humanness_score"] = new_analysis["humanness_score"]
                        regenerated += 1
    print(f"  Quality Gate: {sum(1 for a in gate_results if a['pass'])} pasaron, {len(gate_results) - sum(1 for a in gate_results if a['pass'])} fallaron, {regenerated} regenerados")

    dataset_qr = dataset_quality_report(examples)
    print(f"  Reporte calidad: humanness medio={dataset_qr.get('mean_humanness', 'N/A')}, pass_rate={dataset_qr.get('pass_rate', 'N/A')}")

    stats = compute_stats(examples)
    print(f"\n  Estadísticas del dataset:")
    for k, v in stats.items():
        if k == "top_20_words":
            continue
        print(f"    {k}: {v}")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dataset_name = f"{config.niche}_dataset_{ts}"

    output_dir = os.path.join(config.output_dir, dataset_name)
    os.makedirs(output_dir, exist_ok=True)

    train, val, test = split_dataset(examples, config.train_split, config.val_split, config.test_split)
    print(f"\n  Split: {len(train)} train / {len(val)} val / {len(test)} test")

    all_split_examples = [("train", train), ("validation", val), ("test", test)]
    for split_name, split_data in all_split_examples:
        split_dir = os.path.join(output_dir, split_name)
        os.makedirs(split_dir, exist_ok=True)
        export_all(split_data, split_dir, config.formats)

    all_exported = export_all(examples, output_dir, config.formats)
    print(f"\n  Exportado en {output_dir}:")
    for fmt, fpath in all_exported.items():
        size = os.path.getsize(fpath)
        print(f"    {fmt}: {os.path.relpath(fpath)} ({size / 1024:.1f} KB)")

    card = generate_dataset_card(examples, config, stats, dataset_name)
    card_path = os.path.join(output_dir, "README.md")
    with open(card_path, "w", encoding="utf-8") as f:
        f.write(card)
    print(f"    dataset_card: {os.path.relpath(card_path)}")

    metadata = {
        "dataset_name": dataset_name,
        "niche": config.niche,
        "generated_at": datetime.now().isoformat(),
        "num_examples": len(examples),
        "num_train": len(train),
        "num_val": len(val),
        "num_test": len(test),
        "humanization_level": config.humanization_level,
        "watermark": config.watermark_key,
        "quality_gate": {
            "mean_humanness": dataset_qr.get("mean_humanness"),
            "pass_rate": dataset_qr.get("pass_rate"),
            "dataset_passes": dataset_qr.get("dataset_passes"),
            "min_score": dataset_qr.get("min_score"),
            "max_score": dataset_qr.get("max_score"),
        },
        "regenerated_count": regenerated,
        "stats": {k: v for k, v in stats.items() if k != "top_20_words"},
        "formats": config.formats,
    }
    meta_path = os.path.join(output_dir, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"    metadata: {os.path.relpath(meta_path)}")

    print(f"\n  Dataset '{dataset_name}' completado.")
    print(f"  Ubicación: {output_dir}")
    print(f"{'='*60}\n")

    return {
        "dataset_name": dataset_name,
        "output_dir": output_dir,
        "examples": examples,
        "train": train,
        "val": val,
        "test": test,
        "stats": stats,
        "formats": all_exported,
        "metadata": metadata,
    }


def upload_to_hub(config, result):
    """Upload dataset to Hugging Face Hub"""
    from huggingface_hub import HfApi
    if not config.hf_token or not config.hf_username:
        print("HF_TOKEN/HF_USERNAME no configurados. Omitiendo subida.")
        return
    try:
        api = HfApi()
        repo_id = f"{config.hf_username}/{result['dataset_name']}"
        api.create_repo(repo_id=repo_id, repo_type="dataset", exist_ok=True, token=config.hf_token)
        for fmt, fpath in result["formats"].items():
            api.upload_file(
                path_or_fileobj=fpath,
                path_in_repo=os.path.basename(fpath),
                repo_id=repo_id,
                repo_type="dataset",
                token=config.hf_token,
            )
        card_path = os.path.join(result["output_dir"], "README.md")
        api.upload_file(
            path_or_fileobj=card_path,
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type="dataset",
            token=config.hf_token,
        )
        meta_path = os.path.join(result["output_dir"], "metadata.json")
        api.upload_file(
            path_or_fileobj=meta_path,
            path_in_repo="metadata.json",
            repo_id=repo_id,
            repo_type="dataset",
            token=config.hf_token,
        )
        print(f"  Subido a: https://huggingface.co/datasets/{repo_id}")
    except Exception as e:
        print(f"  Error en subida: {e}")
