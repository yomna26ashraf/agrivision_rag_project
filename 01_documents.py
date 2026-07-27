# ══════════════════════════════════════════════════════════════
# 01_documents.py
# بناء الكوربس (documents) من بيانات AgriVision الزراعية الحقيقية
# (cucumber.json, corn.json, strawberry.json) بدل مجال جديد من الصفر
# ══════════════════════════════════════════════════════════════
# كل سجل مرض بيتحول لـ "document" بنفس الشكل المطلوب في تعليمات
# المشروع: id, title, is_current, text. أضفنا كمان حقل "crop" إضافي
# مفيد للفلترة لاحقًا لو حبينا.
#
# ✅ ضيفنا مستند واحد "outdated" عن قصد (توصية مبيد قديمة اتلغت)
#    عشان نحافظ على آلية اختبار current-vs-outdated زي النموذج الأصلي.

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent

CROP_FILES = {
    "Cucumber": "cucumber.json",
    "Corn": "corn.json",
    "Strawberry": "strawberry.json",
}


def _load_json(filename):
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


def _join(value):
    if isinstance(value, list):
        return ". ".join(str(v) for v in value if v)
    return str(value) if value else ""


def _record_to_text(record: dict) -> str:
    """
    بناء نص موحّد للمستند من سجل مرض - بيتعامل مع اختلاف الحقول بين
    ملفات cucumber/corn (schema واحد) وملف strawberry (schema مختلف شوية).
    """
    disease_name = record.get("disease") or record.get("class_name") or "Unknown"
    scientific = record.get("scientific_name", "")
    pathogen = record.get("pathogen", "")
    symptoms = _join(record.get("symptoms"))
    favorable = _join(record.get("favorable_conditions"))
    prevention = _join(record.get("prevention"))
    treatment = _join(record.get("treatment"))
    description = record.get("description", "")  # موجودة في strawberry.json بس
    integrated_mgmt = _join(record.get("integrated_management"))  # strawberry.json

    parts = [
        f"Disease: {disease_name} ({scientific}).",
        f"Pathogen: {pathogen}." if pathogen else "",
        f"Description: {description}" if description else "",
        f"Symptoms: {symptoms}" if symptoms else "",
        f"Favorable conditions for spread: {favorable}" if favorable else "",
        f"Treatment: {treatment}" if treatment else "",
        f"Integrated management: {integrated_mgmt}" if integrated_mgmt else "",
        f"Prevention: {prevention}" if prevention else "",
    ]
    return " ".join(p for p in parts if p)


def _build_documents_for_crop(crop: str, filename: str) -> list:
    records = _load_json(filename)
    documents = []
    for i, record in enumerate(records):
        disease_name = record.get("disease") or record.get("class_name") or f"record_{i}"
        doc_id = f"{crop.lower()}_{disease_name.lower().replace(' ', '_')}"
        documents.append(
            {
                "id": doc_id,
                "title": f"{crop} — {disease_name}",
                "crop": crop,
                "is_current": True,
                "text": _record_to_text(record),
            }
        )
    return documents


documents = []
for crop_name, filename in CROP_FILES.items():
    documents.extend(_build_documents_for_crop(crop_name, filename))

# مستند واحد "outdated" عن قصد - لاختبار آلية current-vs-outdated
# (تماثل مثال "printing_prices_old" في النموذج المرجعي الأصلي)
documents.append(
    {
        "id": "cucumber_pesticide_archived_notice",
        "title": "Archived Pesticide Guidance (Cucumber)",
        "crop": "Cucumber",
        "is_current": False,
        "text": (
            "Archived notice: Endosulfan was previously recommended for cucumber pest control. "
            "This chemical has since been banned in Egypt and many other countries due to environmental "
            "and health hazards. This notice is no longer current and should not be followed."
        ),
    }
)

if __name__ == "__main__":
    print(f"إجمالي عدد المستندات: {len(documents)}")
    from collections import Counter
    print(Counter(d["crop"] for d in documents))
