"""Verificación completa del sistema Data Factory v2"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

errors = []
warnings = []

def check(condition, msg):
    if not condition:
        errors.append(msg)

# 1. Verificar imports
try:
    from src.config import Config, VALID_NICHES
    from src.templates import NICHES, NICHE_KEYS, NICHE_CATEGORIES
    from src.humanizer import Humanizer
    from src.models import BaseProvider, HFProvider, FallbackProvider, create_providers
    from src.quality import filter_examples, deduplicate, compute_stats, generate_dataset_card, watermark_text
    from src.formats import export_all, split_dataset
    from src.pipeline import run_pipeline
    print("[OK] Todos los imports funcionan")
except Exception as e:
    errors.append(f"Error en imports: {e}")

# 2. Verificar configuración
try:
    cfg = Config()
    cfg.validate()
    print(f"[OK] Config por defecto: niche={cfg.niche}, num={cfg.num_examples}")
except Exception as e:
    errors.append(f"Error en config: {e}")

# 3. Verificar nichos
check(len(NICHES) >= 25, f"Solo {len(NICHES)} nichos, deberían ser 25+")
for niche_name, niche_info in NICHES.items():
    check("prompts" in niche_info, f"{niche_name} sin prompts")
    check(len(niche_info["prompts"]) >= 4, f"{niche_name} solo {len(niche_info['prompts'])} prompts")
    check("variables" in niche_info, f"{niche_name} sin variables")
    for var_name, var_values in niche_info["variables"].items():
        check(len(var_values) > 0, f"{niche_name}:{var_name} vacío")
print(f"[OK] {len(NICHES)} nichos validados")

# 4. Verificar categorías
cats = set()
for n in NICHE_KEYS:
    cats.add(NICHES[n].get("category", "unknown"))
check(len(cats) >= 8, f"Solo {len(cats)} categorías, deberían ser 8+")
print(f"[OK] {len(cats)} categorías")

# 5. Verificar humanizer
h = Humanizer(level="extreme", country="México")
test_text = "El paciente llegó con dolor de cabeza y fiebre. El médico le recetó medicamento. El paciente preguntó sobre los efectos secundarios."
result = h.humanize(test_text)
check(result != test_text, "Humanizer no modificó el texto")
check(len(result) > 0, "Humanizer devolvió vacío")
analysis = h.analyze_humanness(result)
check(analysis["humanness_score"] > 0, f"Humanidad baja: {analysis}")
print(f"[OK] Humanizer: score humano={analysis['humanness_score']}")

# 6. Verificar proveedores
providers = create_providers(cfg)
check(len(providers) >= 1, "No se crearon proveedores")
has_fallback = any(isinstance(p, FallbackProvider) for p in providers)
check(has_fallback, "No hay FallbackProvider")
print(f"[OK] {len(providers)} proveedores creados (incluyendo fallback local)")

# 7. Verificar fallback provider
fb = FallbackProvider(cfg)
ex = fb.generate(1)
check(ex is not None, "Fallback no generó ejemplo")
check(len(ex.get("text", "")) > 10, f"Texto generado muy corto: {ex.get('text', '')[:50]}")
print(f"[OK] Fallback genera texto correctamente")

# 8. Verificar quality
examples = [fb.generate(i) for i in range(10)]
filtered = filter_examples(examples)
check(len(filtered) <= len(examples), "filter_examples añadió ejemplos")
deduped = deduplicate(examples)
check(len(deduped) <= len(examples), "dedup añadió ejemplos")
stats = compute_stats(examples)
check(stats["total_examples"] > 0, "Stats vacío")
print(f"[OK] Quality: {len(filtered)} filtrados, {len(deduped)} dedup, stats OK")

# 9. Verificar formats
import tempfile
with tempfile.TemporaryDirectory() as tmp:
    exported = export_all(examples, tmp, ["jsonl", "csv", "alpaca", "sharegpt", "openai", "chatml"])
    for fmt in ["jsonl", "csv", "alpaca", "sharegpt", "openai", "chatml"]:
        check(fmt in exported, f"Formato {fmt} no exportado")
        check(os.path.exists(exported[fmt]), f"Archivo {fmt} no existe")
print(f"[OK] Todos los formatos exportan correctamente")

# 10. Verificar watermark
original = "muy bueno casa trabajo amigo comida dinero bonito grande pequeño"
watermarked = watermark_text(original, "test-key")
check(len(watermarked) > 0, "Watermark devolvió vacío")
check("muy" in original or "casa" in original, "Texto de prueba sin palabras watermarkeables")
# Check at least one word changed
words_orig = set(original.lower().split())
words_wm = set(watermarked.lower().split())
check(words_orig != words_wm or watermarked != original, "Watermark debería modificar algunas palabras")
print(f"[OK] Watermark funcional (original: '{original[:40]}...' -> '{watermarked[:40]}...')")

# 11. Verificar dataset card
card = generate_dataset_card(examples, cfg, stats, "test_dataset")
check("---" in card, "Card sin front matter YAML")
check("Descripción" in card, "Card sin descripción")
check("Licencia" in card, "Card sin licencia")
print(f"[OK] Dataset cards generadas")

# 12. Verificar compatibilidad con CLI
try:
    from generate_dataset import main
    print("[OK] CLI entry point disponible")
except Exception as e:
    warnings.append(f"CLI: {e}")

# 13. Verificar pipeline completo (modo dry run con 5 ejemplos)
try:
    cfg_small = Config()
    cfg_small.niche = "medical"
    cfg_small.num_examples = 5
    cfg_small.formats = ["jsonl"]
    cfg_small.val_split = 0.1
    cfg_small.test_split = 0.1
    result = run_pipeline(cfg_small)
    check(result is not None, "Pipeline devolvió None")
    if result:
        check(len(result["examples"]) > 0, "Pipeline no generó ejemplos")
        check(os.path.exists(result["output_dir"]), "Directorio de output no existe")
        print(f"[OK] Pipeline completo: {len(result['examples'])} ejemplos en {result['output_dir']}")
except Exception as e:
    errors.append(f"Pipeline falló: {e}")
    import traceback
    traceback.print_exc()

# RESUMEN
print(f"\n{'='*50}")
print(f"  RESULTADOS:")
print(f"  {'[OK]' if not errors else '[FAIL]'} Errores: {len(errors)}")
print(f"  {'[OK]' if not warnings else '[WARN]'} Advertencias: {len(warnings)}")
if errors:
    print(f"\n  ERRORES:")
    for e in errors:
        print(f"    - {e}")
if warnings:
    print(f"\n  ADVERTENCIAS:")
    for w in warnings:
        print(f"    - {w}")
print(f"{'='*50}")

sys.exit(1 if errors else 0)
