# ══════════════════════════════════════════════════════════════
# calibrate_threshold.py
# سكريبت مؤقت بس - شغّليه مرة واحدة عشان نعرف الأرقام الحقيقية
# لـ raw_embedding_score على جهازك (بعد تغيير الموديل للمتعدد اللغات)
# قبل ما نثبّت رقم الـ threshold النهائي في 06_retrieve_context.py
# ══════════════════════════════════════════════════════════════

from importlib import import_module

hybrid_search = import_module("04_vector_representation").hybrid_search
translate_to_english = import_module("07_prompting").translate_to_english

test_cases = [
    ("سؤال فاضي تمامًا (المفروض score واطي جدًا)", "you love me?"),
    ("سؤال حقيقي - عربي فقط (المفروض score عالي بعد الترجمة)", "ليه ورق الخيار بيصفر وعليه بياض تحت الورقة؟"),
    ("سؤال حقيقي - إنجليزي (المفروض score عالي)", "Why do cucumber leaves turn yellow with white powder underneath?"),
    ("سؤال حقيقي لكن غير مغطى (Endosulfan)", "Is Endosulfan safe for cucumber pests?"),
]

print(f"{'السؤال':<55} | {'بعد الترجمة':<55} | أعلى raw_embedding_score")
print("-" * 140)
for label, question in test_cases:
    translated = translate_to_english(question)
    results = hybrid_search(translated, k=3)
    top_score = max(r["raw_embedding_score"] for r in results)
    print(f"{label:<55} | {translated:<55} | {top_score:.3f}   (أفضل تطابق: {results[0]['title']})")
