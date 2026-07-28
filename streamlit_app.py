from importlib import import_module

import streamlit as st

rag = import_module("07_prompting")

import openai

try:
    if "OPENROUTER_API_KEY" in st.secrets:
        rag.OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
        openai.api_key = st.secrets["OPENROUTER_API_KEY"]  # <--- ضيفي السطر ده
    if "OPENROUTER_MODEL" in st.secrets:
        rag.OPENROUTER_MODEL = st.secrets["OPENROUTER_MODEL"]
except Exception:
    pass
    
st.set_page_config(page_title="AgriVision RAG Assistant", page_icon="🌱")
st.title("🌱 AgriVision — Agricultural Disease Assistant")
st.caption("Ask about cucumber, corn, or strawberry diseases in English or Arabic.")

question = st.text_area("Question", placeholder="e.g. Why do cucumber leaves turn yellow with brown spots?")

if st.button("Answer") and question.strip():
    with st.spinner("Retrieving context and generating answer..."):
        answer, sources = rag.answer_question(question)

    st.text_area("Answer", value=answer, height=220)

    with st.expander(f"Sources ({len(sources)})"):
        for source in sources:
            status = "🟢 CURRENT" if source["is_current"] else "🔴 OUTDATED"
            st.markdown(f"**{source['title']}** — {status} (score: {source['score']:.3f})")
            st.write(source["chunk_text"])
            st.divider()
