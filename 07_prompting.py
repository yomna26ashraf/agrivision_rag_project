# ══════════════════════════════════════════════════════════════
# 07_prompting.py
# نفس نمط النموذج المرجعي - OpenRouter API، مفتاح من متغيرات البيئة
# أو Streamlit secrets وقت النشر (أبدًا مش مكتوب في الكود).
# ══════════════════════════════════════════════════════════════

from importlib import import_module
import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

build_context = import_module("06_retrieve_context").build_context

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")


def translate_to_english(text: str) -> str:
    """
    ترجمة سريعة للسؤال للإنجليزي قبل البحث فقط (مش قبل توليد الإجابة
    النهائية) - عشان نضمن تطابق لغوي حقيقي مع الكوربس (المكتوب
    بالإنجليزي بالكامل)، بدل ما نراهن على قدرة موديل الـ embeddings
    على المواءمة الدلالية عبر لغتين لمصطلحات زراعية تقنية دقيقة.
    """
    if not OPENROUTER_API_KEY:
        return text  # fallback: من غير مفتاح، سيبي النص زي ما هو

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)
    try:
        response = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[{
                "role": "user",
                "content": (
                    "Translate the following question to English. "
                    "Reply with ONLY the translated question, nothing else.\n\n"
                    f"{text}"
                ),
            }],
            temperature=0,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return text  # لو الترجمة فشلت لأي سبب، كملي بالنص الأصلي بدل ما تقفي


def build_prompt(question, context):
    return f"""You are a careful grounded agricultural assistant for Egyptian farmers.
Use only the provided context.
If the context is not enough, say you do not know rather than guessing.
Prefer CURRENT sources over OUTDATED sources, and mention if a source is outdated.
Cite sources like [Source 1].

Question:
{question}

Context:
{context}
"""


def ask_openrouter(prompt):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY or st.secrets.get("OPENROUTER_API_KEY", ""),
    )
    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content


def answer_question(question):
    search_query = translate_to_english(question)  # البحث بالإنجليزي دايمًا
    context, sources = build_context(search_query)
    prompt = build_prompt(question, context)  # الإجابة بلغة السؤال الأصلي

    if not context:
        return (
            "معلش، مفيش عندي معلومات كافية عن السؤال ده في قاعدة المعرفة الحالية "
            "(الخيار، الذرة، الفراولة).",
            sources,
        )

    if not OPENROUTER_API_KEY:
        return "Missing OPENROUTER_API_KEY.", sources

    return ask_openrouter(prompt), sources
