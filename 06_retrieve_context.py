# ══════════════════════════════════════════════════════════════
# 06_retrieve_context.py
# بناء حزمة السياق (Context Package): تفضيل current، إزالة تكرار،
# ترقيم المصادر [Source N] - نفس منهجية النموذج المرجعي بالضبط.
# ══════════════════════════════════════════════════════════════

from importlib import import_module

hybrid_search = import_module("04_vector_representation").hybrid_search

# حد أدنى مطلق للـ cosine similarity (قبل أي تطبيع نسبي) - أي نتيجة
# أضعف من كده معناها "مفيش علاقة حقيقية بالسؤال" حتى لو طلعت أعلى
# نتيجة نسبيًا بين الـ chunks التانية لنفس السؤال.
# ✅ رقم نهائي مبني على قياس حقيقي (calibrate_threshold.py):
#    سؤال فاضي تمامًا -> 0.056  |  أضعف سؤال حقيقي مغطى -> 0.614
#    0.35 يفصل بينهم بهامش أمان مريح على الجانبين
#MIN_RAW_EMBEDDING_SCORE = 0.35
# قللي الرقم عشان يراعي الاختلافات بين البيئات (أو خليه 0.0 يلغيه تماماً):
MIN_RAW_EMBEDDING_SCORE = 0.10

def build_context(question, k=8, max_sources=3):
    rows = hybrid_search(question, k=k)

    # 🚪 بوابة الفلترة المطلقة - قبل أي ترتيب أو تفضيل current/outdated
    rows = [row for row in rows if row["raw_embedding_score"] >= MIN_RAW_EMBEDDING_SCORE]

    # ✅ إصلاح: current بقى "أفضلية بسيطة" (+0.05) مش استبعاد قطعي.
    # قبل كده: (is_current, score) بترتب current قبل outdated دايمًا
    # بغض النظر عن قوة score - فمستند زي "Archived Pesticide Guidance"
    # كان بيتسحب تلقائيًا حتى لو كان الأعلى صلة فعليًا بالسؤال.
    CURRENT_BONUS = 0.05
    rows = sorted(
        rows,
        key=lambda row: row["score"] + (CURRENT_BONUS if row["is_current"] else 0),
        reverse=True,
    )

    selected = []
    seen_documents = set()

    for row in rows:
        if row["score"] <= 0:
            continue
        if row["document_id"] in seen_documents:
            continue
        selected.append(row)
        seen_documents.add(row["document_id"])
        if len(selected) == max_sources:
            break

    context = ""
    for source_number, row in enumerate(selected, start=1):
        status = "CURRENT" if row["is_current"] else "OUTDATED"
        context += f"[Source {source_number}] {row['title']} ({status})\n{row['chunk_text']}\n\n"

    return context.strip(), selected
