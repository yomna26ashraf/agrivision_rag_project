# AgriVision RAG Assistant — Student RAG Project

مشروع RAG بسيط (بحسب متطلبات التسليم) مبني على بيانات AgriVision الزراعية
الحقيقية (الخيار، الذرة، الفراولة) بدل مجال جديد من الصفر.

```text
documents (51 مستند من cucumber.json + corn.json + strawberry.json)
-> preprocessing (تنظيف + lemmatization)
-> chunking (نوافذ كلمات متداخلة، 60 كلمة + تداخل 15)
-> vector representation (Hybrid: 0.4×BM25 + 0.6×all-MiniLM-L6-v2)
-> vector store (ChromaDB)
-> context retrieval (تفضيل current، إزالة تكرار، ترقيم مصادر)
-> prompting (OpenRouter، إجابة مؤسَّسة على السياق فقط)
-> Streamlit UI
```

## التشغيل محليًا

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# افتحي .env وحطي مفتاح OpenRouter الحقيقي بتاعك
python 05_create_chroma_store.py
streamlit run streamlit_app.py
```

## ملاحظة مهمة عن current-vs-outdated
ضفنا عن قصد مستند واحد "outdated" (`Archived Pesticide Guidance`) عن مبيد
(Endosulfan) اتحظر فعليًا في مصر ودول تانية، عشان نختبر إن النظام بيفضّل
المصادر الحالية حتى لو المستند القديم طلع score أعلى في البحث الخام.

## النشر على Streamlit Cloud
1. ارفعي المشروع على GitHub (تأكدي إن `.env` مش متضاف بفضل `.gitignore`)
2. من Streamlit Cloud: New app → اختاري الـ repo → Deploy
3. من Manage app → Secrets، ضيفي:
   ```toml
   OPENROUTER_API_KEY = "gsk_... أو مفتاح OpenRouter الحقيقي"
   OPENROUTER_MODEL = "openai/gpt-4o-mini"
   ```

## التسليم النهائي
- ZIP لهذا المجلد (بعد حذف `chroma_db/` و`.env` الحقيقي)
- رابط GitHub repo
- رابط تطبيق Streamlit المنشور
